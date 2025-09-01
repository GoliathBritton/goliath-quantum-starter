/**
 * MCP Client for NQBA Integration
 * Handles communication with the NQBA MCP system
 */

export interface MCPToolCall {
  tool: string
  payload: any
}

export interface MCPResponse {
  success: boolean
  data?: any
  error?: string
}

export class MCPClient {
  private baseUrl: string
  private apiKey: string

  constructor(baseUrl: string = process.env.NEXT_PUBLIC_NQBA_MCP_ENDPOINT || 'http://localhost:8000/mcp', apiKey: string = process.env.NEXT_PUBLIC_NQBA_API_KEY || '') {
    this.baseUrl = baseUrl
    this.apiKey = apiKey
  }

  /**
   * Call an MCP tool
   */
  async callTool(tool: string, payload: any): Promise<MCPResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/${tool}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`,
          'X-NQBA-Version': '1.0.0'
        },
        body: JSON.stringify(payload),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return {
        success: true,
        data
      }
    } catch (error) {
      console.error('MCP tool call failed:', error)
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      }
    }
  }

  /**
   * Get available MCP tools
   */
  async getAvailableTools(): Promise<MCPResponse> {
    return this.callTool('list_tools', {})
  }

  /**
   * Deploy quantum sales agents
   */
  async deploySalesAgents(config: {
    agentCount: number
    contactList: any[]
    campaignType: string
    channels: string[]
  }): Promise<MCPResponse> {
    return this.callTool('deploy_sales_agents', config)
  }

  /**
   * Get agent performance metrics
   */
  async getAgentMetrics(agentIds: string[]): Promise<MCPResponse> {
    return this.callTool('get_agent_metrics', { agent_ids: agentIds })
  }

  /**
   * Optimize campaign with quantum computing
   */
  async optimizeCampaign(campaignData: any): Promise<MCPResponse> {
    return this.callTool('optimize_campaign', campaignData)
  }

  /**
   * Enrich contact data
   */
  async enrichContacts(contacts: any[]): Promise<MCPResponse> {
    return this.callTool('enrich_contacts', { contacts })
  }

  /**
   * Get quantum computing status
   */
  async getQuantumStatus(): Promise<MCPResponse> {
    return this.callTool('get_quantum_status', {})
  }

  /**
   * Test Dynex connection
   */
  async testDynexConnection(): Promise<MCPResponse> {
    return this.callTool('test_dynex', {})
  }
}

// Default instance
export const mcpClient = new MCPClient()

// Utility function for direct tool calls
export async function callMCPTool(tool: string, payload: any): Promise<MCPResponse> {
  return mcpClient.callTool(tool, payload)
}
