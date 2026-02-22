
export type AgentRole = 'workflow' | 'sql' | 'rag' | 'seller' | 'ops' | 'fraud';

export interface Agent {
  id: AgentRole;
  name: string;
  description: string;
  icon: string;
  color: string;
}

export interface NotificationDetails {
  to: string;
  subject: string;
  body: string;
  status: string;
  timestamp: string;
}

export interface Notification {
  type: 'email';
  recruit: string;
  details: NotificationDetails;
}


export interface Document {
  id: string;
  name: string;
  type: string;
  content: string;
  size: string;
  uploadedAt: Date;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  agent?: AgentRole;
  content: any;
  timestamp: Date;
  sources?: string[];
}

export interface Product {
  id: number;
  name: string;
  price: number;
  stock: number;
  category: string;
  seller: string;
  rating: number;
  description?: string;
  sku?: string;
  origin?: string;
}

export interface Order {
  id: string;
  product: string;
  amount: number;
  status: 'Delivered' | 'Pending' | 'Shipped';
  date: string;
  customerName?: string;
  shippingAddress?: string;
  trackingId?: string;
}

export interface Toast {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info';
}

export interface EmailConfig {
  recipientEmail: string;
  enabled: boolean;
}
