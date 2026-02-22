
import { Agent, Product, Order } from './types';

export const AGENTS: Agent[] = [
  { id: 'workflow', name: 'Workflow Master • ዋና አስተዳዳሪ', description: 'Intelligently routes tasks to specialized agents.', icon: 'fa-network-wired', color: 'bg-ethiGreen' },
  { id: 'sql', name: 'Data Analyst • የመረጃ ተንታኝ', description: 'Expert in marketplace inventory and sales data.', icon: 'fa-database', color: 'bg-blue-600' },
  { id: 'rag', name: 'Knowledge Specialist • የእውቀት ባለሙያ', description: 'Answers questions from documents and policies.', icon: 'fa-book', color: 'bg-ethiGold' },
  { id: 'seller', name: 'Seller Consultant • የሻጭ አማካሪ', description: 'Advises on pricing and market strategies.', icon: 'fa-chart-line', color: 'bg-orange-600' },
  { id: 'ops', name: 'Operations Manager • የክንውን ስራ አስኪያጅ', description: 'Logistics, delivery tracking and admin tasks.', icon: 'fa-truck-loading', color: 'bg-ethiRed' },
];

export const MOCK_PRODUCTS: Product[] = [
  { id: 1, name: "Premium Teff Flour (5kg) • 优质ጤፍ", price: 2450.0, stock: 120, category: "Grains", seller: "Adane Farms", rating: 4.9 },
  { id: 2, name: "Organic Honey (500g) • ኦርጋኒክ ማር", price: 450.5, stock: 45, category: "Natural Foods", seller: "Zedwitu Honey", rating: 4.7 },
  { id: 3, name: "Cold Pressed Linseed Oil • የተልባ ዘይት", price: 180.0, stock: 15, category: "Oils", seller: "EthioOil", rating: 4.5 },
  { id: 4, name: "Green Coffee Beans (1kg) • ጥሬ ቡና", price: 850.0, stock: 200, category: "Coffee", seller: "Yirgacheffe Coop", rating: 4.9 },
  { id: 5, name: "Handmade Bamboo Basket • ቅርጫት", price: 525.0, stock: 8, category: "Crafts", seller: "Arba Minch Crafts", rating: 4.8 },
];

export const MOCK_ORDERS: Order[] = [
  { id: "ORD-101", product: "Premium Teff Flour", amount: 2450.0, status: 'Delivered', date: '2024-03-10' },
  { id: "ORD-102", product: "Organic Honey", amount: 900.0, status: 'Shipped', date: '2024-03-11' },
  { id: "ORD-103", product: "Green Coffee Beans", amount: 1700.0, status: 'Pending', date: '2024-03-12' },
];

export const AGENT_SYSTEM_PROMPTS = {
  workflow: "You are the Ethi Marketplace mentor. Route queries. You can also trigger emails via the specialized agents. Speak warmly and naturalmente. Use Ethiopian greetings like 'Selam' where appropriate. No markdown.",
  sql: "You are the Data Analyst. Explain figures in plain text using ETB (Birr). You can trigger performance report emails if requested. No asterisks.",
  rag: "You are the Knowledge Assistant. Use provided docs only. No markdown formatting.",
  seller: "You are the Strategic Seller Partner. You provide growth advice for the Ethiopian market and can send promotional offer emails to customers. Use the 'send_email' tool for promotions. No asterisks.",
  ops: "You are the Operations Lead. Address logistics in Ethiopia. You MUST use the 'send_email' tool to notify users about order status changes or shipping delays. No markdown."
};
