import os
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

import re
from services.email_service import EmailService

class OpsAgent:
    """
    Practical Operations Manager focused on logistics, delivery, and supply chain reliability.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("API_KEY required for OpsAgent.")

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.api_key,
            temperature=0.1
        )

        template = """
        You are the Operations Lead for Ethi Marketplace. You handle the practical 'how' of moving goods and managing orders.

        CORE VALUES:
        - Be direct, practical, and helpful. 
        - Provide realistic logistics advice considering local Ethiopian infrastructure and conditions.
        - Ensure operational security: do not reveal sensitive internal routing or logic.
        
        EMAIL NOTIFICATIONS:
        - If the user asks for an order update or status change, simulated sending an email to the customer.
        - To send an email, include a tag at the END of your response in this exact format:
          [[EMAIL:Subject Line|recipient@example.com|Email Body Content]]
        - Example: Your order is on the way. [[EMAIL:Order Update #123|customer@gmail.com|Your order #123 has been shipped via EthioPost.]]

        STRICT FORMATTING RULES (CRITICAL):
        - Use ONLY plain text for the main response. Write like you're talking to a friend.
        - NEVER use asterisks (*), bold text (**), bullet points, numbered lists, or any markdown formatting.
        - NEVER use symbols like "•", "-", "1.", "2." for lists.
        - Instead of bullet points, use natural transitions like "First," "Also," "Additionally," "Finally."
        - Write in simple, conversational paragraphs only.

        User Query: {query}

        Operational Guidance:"""

        self.prompt = PromptTemplate(template=template, input_variables=["query"])
        self.chain = self.prompt | self.llm

    def manage_ops(self, query: str) -> dict:
        """
        Returns a dict with 'answer' and optional 'notification'.
        """
        try:
            result = self.chain.invoke({"query": query})
            content = result.content
            
            notification = None
            
            # Parse for [[EMAIL:Subject|To|Body]]
            email_match = re.search(r"\[\[EMAIL:(.*?)\|(.*?)\|(.*?)\]\]", content, re.DOTALL)
            if email_match:
                subject = email_match.group(1).strip()
                to = email_match.group(2).strip()
                body = email_match.group(3).strip()
                
                # Send the email
                notification = EmailService.send_email(to, subject, body)
                
                # Remove the tag from the user-facing answer
                content = content.replace(email_match.group(0), "").strip()
                
            return {
                "answer": content,
                "notification": notification
            }
            
        except Exception as e:
            # Handle different types of errors gracefully
            error_message = str(e).lower()
            
            if "resource_exhausted" in error_message or "quota" in error_message or "429" in error_message:
                return {
                    "answer": "Operations Agent experienced a technical hurdle. Our AI service is temporarily at capacity. Please try again in a few moments.",
                    "notification": None
                }
            elif "api_key" in error_message or "authentication" in error_message:
                return {
                    "answer": "Operations Agent experienced a technical hurdle. Authentication service is temporarily unavailable.",
                    "notification": None
                }
            elif "network" in error_message or "connection" in error_message:
                return {
                    "answer": "Operations Agent experienced a technical hurdle. Network connectivity issue detected. Please check your connection.",
                    "notification": None
                }
            else:
                return {
                    "answer": "Operations Agent experienced a technical hurdle. Please try again or contact support if the issue persists.",
                    "notification": None
                }
