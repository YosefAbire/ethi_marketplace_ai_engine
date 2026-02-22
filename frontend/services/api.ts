
import { AgentRole, Product, Order, Notification } from "../types";

const API_BASE_URL = "http://127.0.0.1:8000";

export interface BackendResponse {
    agent: AgentRole;
    answer: string;
    sources?: string[];
    query_generated?: string;
    notifications?: Notification[];
}

export const apiService = {
    async login(email: string, password: string): Promise<any> {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Login failed");
        }
        return await response.json();
    },

    async register(name: string, email: string, password: string): Promise<any> {
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, password }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Registration failed");
        }
        return await response.json();
    },

    async ask(prompt: string, role: AgentRole): Promise<BackendResponse> {
        const endpoint = this.getEndpoint(role);

        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ prompt }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Backend request failed");
        }

        const data = await response.json();
        return {
            agent: data.agent,
            answer: data.answer || data.response, // Backward compatibility fallback
            sources: data.sources,
            query_generated: data.query_generated,
            notifications: data.notifications
        };
    },

    async getDocuments(): Promise<any[]> {
        const response = await fetch(`${API_BASE_URL}/rag/documents?t=${new Date().getTime()}`);
        if (!response.ok) throw new Error("Failed to fetch documents");
        return await response.json();
    },

    async uploadFile(file: File): Promise<any> {
        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch(`${API_BASE_URL}/rag/upload`, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Upload failed");
        }
        return await response.json();
    },

    async getDashboardStats(): Promise<any> {
        const response = await fetch(`${API_BASE_URL}/dashboard/stats`);
        if (!response.ok) throw new Error("Failed to fetch dashboard stats");
        return await response.json();
    },

    async getAnalytics() {
        const response = await fetch(`${API_BASE_URL}/dashboard/analytics`);
        if (!response.ok) throw new Error("Failed to fetch analytics");
        return await response.json();
    },

    async searchDashboard(query: string): Promise<any> {
        const response = await fetch(`${API_BASE_URL}/dashboard/search?q=${encodeURIComponent(query)}`);
        if (!response.ok) throw new Error("Failed to search dashboard");
        return await response.json();
    },

    async getProducts(): Promise<Product[]> {
        const response = await fetch(`${API_BASE_URL}/dashboard/products`);
        if (!response.ok) throw new Error("Failed to fetch products");
        return await response.json();
    },

    async getOrders(): Promise<Order[]> {
        const response = await fetch(`${API_BASE_URL}/dashboard/orders`);
        if (!response.ok) throw new Error("Failed to fetch orders");
        return await response.json();
    },

    async deleteDocument(filename: string): Promise<any> {
        const response = await fetch(`${API_BASE_URL}/rag/documents/${encodeURIComponent(filename)}`, {
            method: "DELETE",
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Delete failed");
        }
        return await response.json();
    },

    getEndpoint(role: AgentRole): string {
        switch (role) {
            case "sql": return "/ask";
            case "rag": return "/rag/ask";
            case "seller": return "/seller/ask";
            case "ops": return "/ops/ask";
            case "workflow": return "/workflow/ask";
            case "fraud": return "/fraud/ask";
            default: return "/workflow/ask";
        }
    },

    // Fraud Detection API methods
    async runFraudScan(scanType: string = 'full'): Promise<any> {
        const response = await fetch(`${API_BASE_URL}/fraud/scan`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ scan_type: scanType }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || "Fraud scan failed");
        }
        return await response.json();
    },

    async getFraudAlerts(riskLevel?: string, limit: number = 50): Promise<any> {
        const params = new URLSearchParams();
        if (riskLevel) params.append('risk_level', riskLevel);
        params.append('limit', limit.toString());

        const response = await fetch(`${API_BASE_URL}/fraud/alerts?${params}`);
        if (!response.ok) throw new Error("Failed to fetch fraud alerts");
        return await response.json();
    },

    async getFraudAlertDetails(alertId: string): Promise<any> {
        const response = await fetch(`${API_BASE_URL}/fraud/alerts/${alertId}`);
        if (!response.ok) throw new Error("Failed to fetch alert details");
        return await response.json();
    },

    async updateFraudAlertStatus(alertId: string, status: string, resolvedBy?: string, notes?: string): Promise<any> {
        const response = await fetch(`${API_BASE_URL}/fraud/alerts/${alertId}/status`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status, resolved_by: resolvedBy, notes }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to update alert status");
        }
        return await response.json();
    },

    async getFraudStatistics(days: number = 30): Promise<any> {
        const response = await fetch(`${API_BASE_URL}/fraud/statistics?days=${days}`);
        if (!response.ok) throw new Error("Failed to fetch fraud statistics");
        return await response.json();
    },

    async checkTransaction(transactionData: any): Promise<any> {
        const response = await fetch(`${API_BASE_URL}/fraud/check-transaction`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(transactionData),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Transaction check failed");
        }
        return await response.json();
    },

    async createUserProfile(userId: string): Promise<any> {
        const response = await fetch(`${API_BASE_URL}/fraud/create-user-profile/${userId}`, {
            method: "POST",
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to create user profile");
        }
        return await response.json();
    },

    async submitContactForm(formData: any): Promise<any> {
        const response = await fetch(`${API_BASE_URL}/api/contact`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || errorData.message || "Failed to send message");
        }
        return await response.json();
    }
};
