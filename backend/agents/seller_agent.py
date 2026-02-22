import os
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

from services.email_service import EmailService
import re

class SellerAgent:
    """
    Senior Business Consultant providing strategic advice, category performance 
    analysis, and dynamic pricing optimization using the Data Analyst persona.
    Now localized with deep knowledge of Ethiopian market cycles.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("API_KEY required for SellerAgent.")

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.api_key,
            temperature=0.4
        )

        template = """
        You are a Senior Strategic Seller Partner specializing in the Ethiopian marketplace. 
        Your goal is to provide strategic growth advice that leverages local dynamics.

        LOCAL CONTEXT REQUIREMENTS:
        - Incorporate Ethiopian cultural and religious holidays (like Enkutatash, Meskel, Genna, Timkat, Fasika, and Eid) into marketing and inventory strategies.
        - Account for agricultural cycles (Meher and Belg seasons) and their impact on commodity availability (e.g., Teff harvest peaks, Coffee processing times, Honey collection periods).
        - Consider local consumer behavior during wedding seasons and fasting periods.

        DASHBOARD AWARENESS:
        - You have access to "Sales Trends" (Revenue over time) and "Category Distribution" (Inventory by category) charts on the dashboard.
        - When analyzing performance, explicitly reference these visualizations (e.g., "As the sales trend chart indicates...", "Looking at the category distribution...").

        EMAIL CAMPAIGNS:
        - If the user asks to "notify customers" or "create a campaign", simulate sending a mass email.
        - To send an email, include a tag at the END of your response in this exact format:
          [[EMAIL:Campaign Subject|all_customers@marketplace.com|Campaign Body Content]]

        PROFESSIONAL INTEGRITY:
        - Only give advice relevant to business, pricing, and marketing.
        - Maintain a warm, encouraging, yet professional human tone.

        FORMATTING RULES (CRITICAL):
        - Use plain text ONLY. Write like you're talking to a friend or colleague.
        - NEVER use asterisks (*), bold text (**), markdown symbols, bullet points with symbols, or any formatting.
        - NEVER use numbered lists with symbols like "1." or bullet points like "•" or "-".
        - Instead of bullet points, use natural paragraph breaks and phrases like "First," "Also," "Additionally," "Finally."
        - Structure your advice in simple, readable paragraphs with natural transitions.
        - Write in a conversational, warm tone as if speaking directly to the person.

        User Query: {query}

        Expert Advice:"""

        self.prompt = PromptTemplate(template=template, input_variables=["query"])
        self.chain = self.prompt | self.llm

    def get_advice(self, query: str, data_context: Optional[str] = None) -> dict:
        """
        Main entry point. Intelligently decides between strategic advice, 
        category performance analysis, or pricing optimization.
        Returns dict with 'answer' and optional 'notification'.
        """
        lower_query = query.lower()
        performance_triggers = ["performance", "stats", "best category", "top selling", "sales figures"]
        pricing_triggers = ["price", "pricing", "adjustment", "optimization", "cost", "margin"]
        
        answer = ""
        
        if data_context:
            if any(trigger in lower_query for trigger in pricing_triggers):
                answer = self.optimize_pricing(data_context, query)
                return {"answer": answer, "notification": None}
            if any(trigger in lower_query for trigger in performance_triggers):
                answer = self.get_category_performance(data_context)
                return {"answer": answer, "notification": None}
            
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
                    "answer": "Seller Consultant experienced a technical hurdle. Our AI service is temporarily at capacity. Please try again in a few moments.",
                    "notification": None
                }
            elif "api_key" in error_message or "authentication" in error_message:
                return {
                    "answer": "Seller Consultant experienced a technical hurdle. Authentication service is temporarily unavailable.",
                    "notification": None
                }
            elif "network" in error_message or "connection" in error_message:
                return {
                    "answer": "Seller Consultant experienced a technical hurdle. Network connectivity issue detected. Please check your connection.",
                    "notification": None
                }
            else:
                return {
                    "answer": "Seller Consultant experienced a technical hurdle. Please try again or contact support if the issue persists.",
                    "notification": None
                }

    def get_category_performance(self, sales_data: str) -> str:
        """
        Adopts the Data Analyst persona to analyze marketplace figures with seasonal context.
        """
        analysis_template = """
        SYSTEM: You are the Data Analyst specializing in Ethiopian trade. Explain figures 
        in a clear, conversational plain-text way. Link performance to local events.
        
        Analyze the following performance data. Identify top-selling categories and 
        provide actionable steps for growth, specifically considering if high demand 
        aligns with upcoming Ethiopian holidays or the end of harvest seasons.
        
        CRITICAL FORMATTING RULES: 
        - Plain text ONLY. Write like you're having a conversation with a colleague.
        - NEVER use asterisks (*), bold text (**), bullet points, numbered lists, or any markdown formatting.
        - Instead of bullet points, use natural transitions like "First," "Also," "Additionally," "Finally."
        - Conversational, professional human tone.

        Data to analyze: {sales_data}
        Analysis:"""

        analysis_prompt = PromptTemplate(template=analysis_template, input_variables=["sales_data"])
        chain = analysis_prompt | self.llm
        
        try:
            result = chain.invoke({"sales_data": sales_data})
            return result.content
        except Exception as e:
            error_message = str(e).lower()
            
            if "resource_exhausted" in error_message or "quota" in error_message or "429" in error_message:
                return "I'm temporarily unable to analyze category performance due to high system demand. Please try again in a few moments."
            else:
                return "I couldn't perform the category analysis at this moment. Please try again later."

    def optimize_pricing(self, market_data: str, user_query: str) -> str:
        """
        Analyzes inventory levels and demand to suggest dynamic pricing adjustments 
        synchronized with the Ethiopian calendar.
        """
        pricing_template = """
        SYSTEM: You are the Dynamic Pricing Consultant for the Ethiopian region. 
        Suggest pricing adjustments based on stock, demand, and seasonal proximity.
        
        ANALYSIS GOALS:
        - If an Ethiopian holiday is approaching (e.g., Meskel or Genna), suggest pricing strategies for high-demand items like Honey or Grains.
        - If current stock is from a recent Meher harvest, advise on competitive bulk pricing.
        - Consider if price changes are appropriate for current fasting or non-fasting periods.
        - User request: "{user_query}"
        
        CRITICAL FORMATTING RULES:
        - Plain text ONLY. Write like you're having a conversation with a colleague.
        - NEVER use asterisks (*), bold text (**), bullet points, numbered lists, or any markdown formatting.
        - Instead of bullet points, use natural transitions like "First," "Also," "Additionally," "Finally."
        - Professional, data-driven, yet human conversational tone.
        
        Marketplace Snapshot:
        {market_data}
        
        Pricing Strategy Recommendations:"""

        pricing_prompt = PromptTemplate(template=pricing_template, input_variables=["market_data", "user_query"])
        chain = pricing_prompt | self.llm
        
        try:
            result = chain.invoke({"market_data": market_data, "user_query": user_query})
            return result.content
        except Exception as e:
            error_message = str(e).lower()
            
            if "resource_exhausted" in error_message or "quota" in error_message or "429" in error_message:
                return "I'm temporarily unable to generate pricing recommendations due to high system demand. Please try again in a few moments."
            else:
                return "I couldn't generate pricing recommendations at this time. Please try again later."
