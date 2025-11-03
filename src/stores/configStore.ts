import { create } from 'zustand';
import { ApiConfig } from '../types';
import { loadApiConfig, saveApiConfig } from '../utils/config';

interface ConfigState {
  config: ApiConfig;
  loadConfig: () => void;
  updateConfig: (config: Partial<ApiConfig>) => void;
}

export const useConfigStore = create<ConfigState>((set) => ({
  config: loadApiConfig(),
  
  loadConfig: () => {
    const config = loadApiConfig();
    set({ config });
  },
  
  updateConfig: (newConfig: Partial<ApiConfig>) => {
    set((state) => {
      const updated = { ...state.config, ...newConfig };
      saveApiConfig(updated);
      return { config: updated };
    });
  },
}));

