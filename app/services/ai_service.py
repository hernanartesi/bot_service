from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage, AIMessage
from app.core.config import settings
from app.services.expense_category_service import ExpenseCategoryService
from app.services.expense_service import ExpenseService
from app.schemas.expense import ExpenseCreate
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
    
    async def process_message(self, message: str, user_id: int) -> dict:
        """
        Analyze a natural language expense message, save it to the database, and return structured data.
        If the message cannot be analyzed as an expense, returns a structure with 'unknown' category.
        
        Args:
            message: The expense message to analyze
            user_id: The ID of the user creating the expense
            
        Returns:
            A dictionary with the saved expense data or error information
        """
        try:
            # Analyze the message
            print("Analyzing message: ", message)
            categories = ExpenseCategoryService.get_categories_as_string()
            
            messages = [
                SystemMessage(content=(
                    "You are an assistant that extracts structured expense data from user messages. "
                    "Given a message like 'Bought coffee for 4.5 dollars', extract and return a JSON object "
                    "with the fields: amount (number), category (string), and description (string).\n\n"
                    f"Available categories are: {categories}\n"
                    "If the message cannot be analyzed as an expense, set category to 'unknown'. "
                    "But only if you can't extract an expense, otherwise use a category from the list above. "
                    "Respond only with the JSON structure, for example:\n"
                    '{"amount": 4.5, "category": "Food", "description": "Bought coffee"}'
                )),
                HumanMessage(content=message)
]


            
            try:
                response = self.llm.invoke(messages)
                result = json.loads(response.content)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON response: {e}")
                print("Raw response:", response.content)
                return {
                    'amount': 0,
                    'category': 'unknown',
                    'description': message,
                    'error': 'Could not parse AI response'
                }
            except Exception as e:
                print(f"Error calling OpenAI: {e}")
                return {
                    'amount': 0,
                    'category': 'unknown',
                    'description': message,
                    'error': str(e)
                }
            
            # Ensure the result has the expected structure
            if not isinstance(result, dict) or not all(key in result for key in ['amount', 'category', 'description']):
                print("Invalid response structure:", result)
                return {
                    'amount': 0,
                    'category': 'unknown',
                    'description': message,
                    'error': 'Could not analyze message as expense'
                }
            
            # Validate category
            if result['category'] not in categories.split(", ") and result['category'] != 'unknown':
                print(f"Invalid category: {result['category']}")
                result['category'] = 'Other'
            
            # Create and save the expense
            try:
                expense_data = ExpenseCreate(
                    user_id=user_id,
                    description=result['description'],
                    amount=float(result['amount']),
                    category=result['category']
                )
                
                saved_expense = ExpenseService.create_expense(expense_data)
                if not saved_expense:
                    return {
                        'amount': 0,
                        'category': 'unknown',
                        'description': message,
                        'error': 'Failed to save expense'
                    }
                
                return {
                    'amount': float(saved_expense.amount),
                    'category': saved_expense.category,
                    'description': saved_expense.description
                }
            except Exception as e:
                print(f"Error saving expense: {e}")
                return {
                    'amount': 0,
                    'category': 'unknown',
                    'description': message,
                    'error': f'Failed to save expense: {str(e)}'
                }
                
        except Exception as e:
            print(f"Unexpected error in process_message: {e}")
            return {
                'amount': 0,
                'category': 'unknown',
                'description': message,
                'error': str(e)
            } 