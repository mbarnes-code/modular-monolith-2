// Service adapters for external integrations
export class OrchestratorAdapter {
  private baseUrl: string;

  constructor(baseUrl: string = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  async getStatus(): Promise<{ status: string }> {
    const response = await fetch(`${this.baseUrl}/health`);
    return response.json();
  }
}

export class LLMAdapter {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  async generate(prompt: string): Promise<{ response: string }> {
    const response = await fetch(`${this.baseUrl}/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt }),
    });
    return response.json();
  }
}
