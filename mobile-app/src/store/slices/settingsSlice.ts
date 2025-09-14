import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface SettingsState {
  theme: 'light' | 'dark' | 'auto';
  language: string;
  notifications: {
    push: boolean;
    email: boolean;
    sms: boolean;
  };
  privacy: {
    analytics: boolean;
    crashReporting: boolean;
    dataSharing: boolean;
  };
  security: {
    biometricAuth: boolean;
    twoFactorAuth: boolean;
    sessionTimeout: number;
  };
  trading: {
    confirmations: boolean;
    riskWarnings: boolean;
    autoLogout: number;
  };
}

const initialState: SettingsState = {
  theme: 'auto',
  language: 'en',
  notifications: {
    push: true,
    email: true,
    sms: false,
  },
  privacy: {
    analytics: true,
    crashReporting: true,
    dataSharing: false,
  },
  security: {
    biometricAuth: false,
    twoFactorAuth: false,
    sessionTimeout: 30,
  },
  trading: {
    confirmations: true,
    riskWarnings: true,
    autoLogout: 15,
  },
};

const settingsSlice = createSlice({
  name: 'settings',
  initialState,
  reducers: {
    setTheme: (state, action: PayloadAction<'light' | 'dark' | 'auto'>) => {
      state.theme = action.payload;
    },
    setLanguage: (state, action: PayloadAction<string>) => {
      state.language = action.payload;
    },
    updateNotificationSettings: (state, action: PayloadAction<Partial<SettingsState['notifications']>>) => {
      state.notifications = { ...state.notifications, ...action.payload };
    },
    updatePrivacySettings: (state, action: PayloadAction<Partial<SettingsState['privacy']>>) => {
      state.privacy = { ...state.privacy, ...action.payload };
    },
    updateSecuritySettings: (state, action: PayloadAction<Partial<SettingsState['security']>>) => {
      state.security = { ...state.security, ...action.payload };
    },
    updateTradingSettings: (state, action: PayloadAction<Partial<SettingsState['trading']>>) => {
      state.trading = { ...state.trading, ...action.payload };
    },
    resetSettings: () => initialState,
  },
});

export const {
  setTheme,
  setLanguage,
  updateNotificationSettings,
  updatePrivacySettings,
  updateSecuritySettings,
  updateTradingSettings,
  resetSettings,
} = settingsSlice.actions;

export default settingsSlice.reducer;