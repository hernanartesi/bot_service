from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage, AIMessage
from app.core.config import settings
from app.services.expense_category_service import ExpenseCategoryService
from app.services.expense_service import ExpenseService
from app.schemas.expense import ExpenseCreate
from app.schemas.message import MessageResponse, ExpenseData, SummaryData
from langchain_core.messages import SystemMessage, HumanMessage
import json

class AIService:
    def __init__(self):
        try:
            self.llm = ChatOpenAI(
                api_key=settings.OPENAI_API_KEY,
                model_name=settings.OPENAI_MODEL_NAME,
                temperature=settings.OPENAI_TEMPERATURE
            )
        except Exception as e:
            print(f"Error initializing ChatOpenAI: {e}")
            raise
    
    async def process_message(self, message: str, user_id: int) -> MessageResponse:
        """
        Analyze a natural language expense message, save it to the database, and return structured data.
        If the message cannot be analyzed as an expense, returns a structure with 'unknown' category.
        
        Args:
            message: The expense message to analyze
            user_id: The ID of the user creating the expense
            
        Returns:
            A MessageResponse with the appropriate data type
        """
        try:
            # Analyze the message
            print("Analyzing message: ", message)
            categories = ExpenseCategoryService.get_categories_as_string()
            
            messages = [
                SystemMessage(content=(
                    "You are an assistant that extracts structured expense data from user messages. "
                    "Given a message like 'Bought coffee for 4.5 dollars', extract and return a JSON object "
                    "with the fields: type (string: expense or summary), and data (object) with the fields: amount (number), category (string), and description (string).\n\n"
                    "There is another case where the user requests a summary of their expenses for a period of time. It should return a postgreSQL query that will be used to get the data from the database. Table is expenses"
                    "Example: expenses from yesterday should get todays date and subtract 1 day and create the query with that date. "
                    "Example2: expenses from last week should get todays date and subtract 7 days and create the query with that date. "
                    "Example3: expenses from last month should get todays date and subtract 30 days and create the query with that date. "
                    "Table fields are id, user_id, description, amount, category, added_at"
                    f"Available categories are: {categories}\n"
                    f"user id is {user_id}\n"
                    "If the message cannot be analyzed as an expense, set category to 'unknown'. "
                    "But only if you can't extract an expense, otherwise use a category from the list above. "
                    "Respond only with the JSON structure, for example:\n"
                    "For expenses"
                    "{type: 'expense', data: {'amount': 4.5, 'category': 'Food', 'description': 'Bought coffee'}}"
                    "For summaries"
                    "{type: 'summary', data: {'query': 'SELECT * FROM expenses WHERE user_id = 1 AND added_at BETWEEN \'2024-01-01\' AND \'2024-01-31\'}}"
                )),
                HumanMessage(content=message)
            ]
            
            try:
                response = self.llm.invoke(messages)
                result = json.loads(response.content)
                print("Result: ", result)

            except json.JSONDecodeError as e:
                print(f"Error parsing JSON response: {e}")
                print("Raw response:", response.content)
                return MessageResponse(
                    type="error",
                    data=None,
                    error="Could not parse AI response"
                )
            except Exception as e:
                print(f"Error calling OpenAI: {e}")
                return MessageResponse(
                    type="error",
                    data=None,
                    error=str(e)
                )
            
            if result.get('type') == "expense":
                print("Result type: ", result.get('type'))
                # Ensure the result has the expected structure
                if not isinstance(result.get('data'), dict) or not all(key in result.get('data', {}) for key in ['amount', 'category', 'description']):
                    print("Invalid response structure:", result)
                    return MessageResponse(
                        type="error",
                        data=None,
                        error="Could not analyze message as expense"
                    )
            
                # Validate category
                if result['data']['category'] not in categories.split(", ") and result['data']['category'] != 'unknown':
                    print(f"Invalid category: {result['data']['category']}")
                    result['data']['category'] = 'Other'
                
                # Create and save the expense
                try:
                    print("Creating")
                    expense_data = ExpenseCreate(
                        user_id=user_id,
                        description=result['data']['description'],
                        amount=float(result['data']['amount']),
                        category=result['data']['category']
                    )
                    print("Expense data: ", expense_data)
                    saved_expense = ExpenseService.create_expense(expense_data)
                    if not saved_expense:
                        return MessageResponse(
                            type="error",
                            data=None,
                            error="Failed to save expense"
                        )
                    
                    return MessageResponse(
                        type="expense",
                        data=ExpenseData(
                            amount=float(saved_expense.amount),
                            category=saved_expense.category,
                            description=saved_expense.description
                        )
                    )
                
                except Exception as e:
                    print(f"Error saving expense: {e}")
                    return MessageResponse(
                        type="error",
                        data=None,
                        error=f'Failed to save expense: {str(e)}'
                    )

            elif result.get('type') == "summary":
                try:
                    # Execute the query and get results
                    expenses = ExpenseService.execute_expenses_query(user_id)
                    return MessageResponse(
                        type="summary",
                        data=[
                            SummaryData(
                                id=exp.id,
                                description=exp.description,
                                amount=float(exp.amount),
                                category=exp.category,
                                added_at=exp.added_at
                            ) for exp in expenses
                        ]
                    )
                except Exception as e:
                    print(f"Error executing query: {e}")
                    return MessageResponse(
                        type="error",
                        data=None,
                        error=f'Failed to execute query: {str(e)}'
                    )
                
        except Exception as e:
            print(f"Unexpected error in process_message: {e}")
            return MessageResponse(
                type="error",
                data=None,
                error=str(e)
            ) 