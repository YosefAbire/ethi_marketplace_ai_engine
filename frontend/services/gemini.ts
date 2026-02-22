
import { GoogleGenAI, Type, FunctionDeclaration } from "@google/genai";
import { AGENT_SYSTEM_PROMPTS } from "../constants";
import { Document, Product, Order, AgentRole, Message } from "../types";

export class GeminiService {
  async routeAndProcess(
    query: string,
    role: AgentRole,
    docs: Document[],
    products: Product[],
    orders: Order[],
    history: Message[] = [],
    onEmailSent?: (data: { recipient: string, subject: string, body: string }) => void
  ) {
    if (!process.env.API_KEY) throw new Error("MISSING_API_KEY");

    const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
    const model = "gemini-3-flash-preview";

    const docsContext = docs.map(d => `[FILE: ${d.name}]\n${d.content}`).join("\n\n");
    const sqlContext = `[PRODUCTS]\n${JSON.stringify(products)}\n\n[ORDERS]\n${JSON.stringify(orders)}`;
    const historyContext = history.map(m => `${m.role.toUpperCase()}: ${m.content}`).join("\n");

    const sendEmailTool: FunctionDeclaration = {
      name: 'send_email',
      parameters: {
        type: Type.OBJECT,
        description: 'Send a notification email to the user regarding order status or promotional updates.',
        properties: {
          recipient: { type: Type.STRING, description: 'The email address of the recipient.' },
          subject: { type: Type.STRING, description: 'The subject line of the email.' },
          body: { type: Type.STRING, description: 'The body content of the email.' },
        },
        required: ['recipient', 'subject', 'body'],
      },
    };

    try {
      let actualRole = role;
      if (role === 'workflow') actualRole = await this.detectIntentWithLLM(ai, query, history);

      const systemPrompt = `${AGENT_SYSTEM_PROMPTS[actualRole]}\n\nYou have the capability to send emails using the 'send_email' tool. Use it for order updates or promotional strategies.`;

      const response = await ai.models.generateContent({
        model,
        contents: `HISTORY:\n${historyContext}\n\nDOCS:\n${docsContext}\n\nDATA:\n${sqlContext}\n\nQUERY: ${query}`,
        config: {
          systemInstruction: systemPrompt,
          tools: [{ functionDeclarations: [sendEmailTool] }],
        },
      });

      if (response.functionCalls) {
        for (const fc of response.functionCalls) {
          if (fc.name === 'send_email' && onEmailSent) {
            onEmailSent(fc.args as any);
          }
        }
      }

      return { text: response.text || "Action completed.", detectedAgent: actualRole };
    } catch (error: any) {
      console.error(error);
      throw error;
    }
  }

  private async detectIntentWithLLM(ai: GoogleGenAI, query: string, history: Message[]): Promise<AgentRole> {
    const prompt = `Categorize query into [sql, rag, seller, ops]: "${query}"`;
    const response = await ai.models.generateContent({ model: "gemini-3-flash-preview", contents: prompt });
    const target = response.text?.trim().toLowerCase() as AgentRole;
    return ['sql', 'rag', 'seller', 'ops'].includes(target) ? target : 'ops';
  }

  async generateBackendCode() {
    const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
    return (await ai.models.generateContent({
      model: "gemini-3-pro-preview",
      contents: "Generate FastAPI code for Ethi Marketplace with Email Notification support (SMTP/Mock).",
    })).text;
  }
}

export const gemini = new GeminiService();
