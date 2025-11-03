import { create } from 'zustand';
import { TravelPlan, BudgetRecord } from '../types';

interface PlanState {
  plans: TravelPlan[];
  currentPlan: TravelPlan | null;
  loading: boolean;
  setPlans: (plans: TravelPlan[]) => void;
  setCurrentPlan: (plan: TravelPlan | null) => void;
  setLoading: (loading: boolean) => void;
}

export const usePlanStore = create<PlanState>((set) => ({
  plans: [],
  currentPlan: null,
  loading: false,
  setPlans: (plans) => set({ plans }),
  setCurrentPlan: (plan) => set({ currentPlan: plan }),
  setLoading: (loading) => set({ loading }),
}));

interface BudgetState {
  records: BudgetRecord[];
  setRecords: (records: BudgetRecord[]) => void;
}

export const useBudgetStore = create<BudgetState>((set) => ({
  records: [],
  setRecords: (records) => set({ records }),
}));

