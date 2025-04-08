from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage
from app.core.config import settings
from app.services.expense_category_service import ExpenseCategoryService
from app.services.expense_service import ExpenseService
from app.schemas.expense import ExpenseCreate

class AIService:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model_name=settings.OPENAI_MODEL_NAME,
            temperature=settings.OPENAI_TEMPERATURE
        )
    
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
            print(categories)
            
            system_message = SystemMessage(content=(
                "You are an assistant that extracts structured expense data from user messages. "
                "Given a message like 'Bought coffee for 4.5 dollars', extract and return a JSON object "
                "with the fields: amount (number), category (string), and description (string).\n\n"
                f"Categories: {categories}. "
                "If the message cannot be analyzed as an expense, set category to 'unknown'. But only if you can't extract an expense, otherwise use a category from the list. "
                "Respond only with the JSON structure."
            ))
            
            human_message = HumanMessage(content=message)
            
            response = self.llm.invoke([system_message, human_message])
            import json
            result = json.loads(response.content)
            
            # Ensure the result has the expected structure
            if not isinstance(result, dict) or not all(key in result for key in ['amount', 'category', 'description']):
                return {
                    'amount': 0,
                    'category': 'unknown',
                    'description': message,
                    'error': 'Could not analyze message as expense'
                }
            
            # Create and save the expense
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
                'id': saved_expense.id,
                'amount': float(saved_expense.amount),
                'category': saved_expense.category,
                'description': saved_expense.description,
                'added_at': saved_expense.added_at
            }
        except Exception as e:
            # Return unknown structure in case of any error
            return {
                'amount': 0,
                'category': 'unknown',
                'description': message,
                'error': str(e)
            } 