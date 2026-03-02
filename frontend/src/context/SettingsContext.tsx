import React, { createContext, useContext, useState, useEffect } from 'react';

type FontSize = 'small' | 'medium' | 'large';

export type PreferredModel = 'gpt5-1' | 'gemini3' | 'qwen';

interface SettingsContextType {
  fontSize: FontSize;
  setFontSize: (size: FontSize) => void;
  getFontSizeClass: (size: FontSize) => string;
  preferredModel: PreferredModel;
  setPreferredModel: (model: PreferredModel) => void;
}

const SettingsContext = createContext<SettingsContextType | undefined>(undefined);

export const SettingsProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [fontSize, setFontSize] = useState<FontSize>('medium');
  const [preferredModel, setPreferredModel] = useState<PreferredModel>('gpt5-1');

  // Load from local storage on mount
  useEffect(() => {
    const savedSize = localStorage.getItem('app_font_size') as FontSize;
    if (savedSize && ['small', 'medium', 'large'].includes(savedSize)) {
      setFontSize(savedSize);
    }
    const savedModel = localStorage.getItem('preferred_model') as PreferredModel;
    if (savedModel && ['gpt5-1', 'gemini3', 'qwen'].includes(savedModel)) {
      setPreferredModel(savedModel);
    }
  }, []);

  // Save to local storage on change
  useEffect(() => {
    localStorage.setItem('app_font_size', fontSize);
  }, [fontSize]);

  useEffect(() => {
    localStorage.setItem('preferred_model', preferredModel);
  }, [preferredModel]);

  const getFontSizeClass = (size: FontSize) => {
    switch (size) {
      case 'small':
        return 'text-xs';
      case 'large':
        return 'text-base';
      case 'medium':
      default:
        return 'text-sm';
    }
  };

  return (
    <SettingsContext.Provider value={{ fontSize, setFontSize, getFontSizeClass, preferredModel, setPreferredModel }}>
      {children}
    </SettingsContext.Provider>
  );
};

export const useSettings = () => {
  const context = useContext(SettingsContext);
  if (context === undefined) {
    throw new Error('useSettings must be used within a SettingsProvider');
  }
  return context;
};
