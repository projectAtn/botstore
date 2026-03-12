export type Capability =
  | 'memory.read' | 'memory.write' | 'files.read' | 'files.write' | 'files.delete'
  | 'calendar.read' | 'calendar.write' | 'email.read' | 'email.send' | 'message.send'
  | 'social.post' | 'payment.charge' | 'web.search' | 'web.fetch' | 'code.exec';

export interface RuntimeBridge {
  callCapability(capability: Capability, payload: Record<string, unknown>): Promise<unknown>;
}

export interface BotPack {
  id: string;
  capabilities: Capability[];
  policy: { riskLevel: 'low' | 'medium' | 'high' };
}

const SENSITIVE = new Set<Capability>(['email.send','message.send','social.post','payment.charge','files.delete']);

export function approvalRequired(pack: BotPack): boolean {
  if (pack.policy.riskLevel === 'high') return true;
  return pack.capabilities.some(c => SENSITIVE.has(c));
}

export async function installPack(runtime: string, pack: BotPack, userId: string) {
  return {
    runtime,
    userId,
    packId: pack.id,
    approvalRequired: approvalRequired(pack),
    status: approvalRequired(pack) ? 'pending_approval' : 'installed'
  };
}
