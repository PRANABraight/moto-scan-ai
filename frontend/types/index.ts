export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  phone?: string;
  avatar?: string;
  createdAt: Date;
}

export interface DamageAnalysis {
  id: string;
  userId: string;
  imageUri: string;
  analysisDate: Date;
  damageDetected: boolean;
  damageType: DamageType[];
  severity: 'Minor' | 'Moderate' | 'Severe';
  costEstimation: CostEstimation;
  status: 'Processing' | 'Completed' | 'Failed';
  confidence: number;
}

export interface DamageType {
  type: 'Scratch' | 'Dent' | 'Crack' | 'Rust' | 'Paint Damage' | 'Broken Glass';
  location: string;
  severity: 'Minor' | 'Moderate' | 'Severe';
  coordinates: { x: number; y: number; width: number; height: number };
}

export interface CostEstimation {
  totalCost: number;
  laborCost: number;
  partsCost: number;
  paintCost: number;
  breakdown: CostBreakdownItem[];
}

export interface CostBreakdownItem {
  item: string;
  cost: number;
  category: 'Labor' | 'Parts' | 'Paint' | 'Other';
  description: string;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}