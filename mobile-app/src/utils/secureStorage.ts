// Secure storage utility for React Native
// This is a mock implementation for web/development
// In a real React Native app, you would use @react-native-async-storage/async-storage
// or react-native-keychain for secure storage

interface SecureStorage {
  setItem(key: string, value: string): Promise<void>;
  getItem(key: string): Promise<string | null>;
  removeItem(key: string): Promise<void>;
  clear(): Promise<void>;
  getAllKeys(): Promise<string[]>;
}

class MockSecureStorage implements SecureStorage {
  private storage: Map<string, string> = new Map();

  async setItem(key: string, value: string): Promise<void> {
    try {
      // In development/web environment, use localStorage with encryption simulation
      if (typeof window !== 'undefined' && window.localStorage) {
        localStorage.setItem(`secure_${key}`, btoa(value)); // Simple base64 encoding
      } else {
        this.storage.set(key, value);
      }
    } catch (error) {
      console.error('SecureStorage setItem error:', error);
      throw error;
    }
  }

  async getItem(key: string): Promise<string | null> {
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        const item = localStorage.getItem(`secure_${key}`);
        return item ? atob(item) : null; // Simple base64 decoding
      } else {
        return this.storage.get(key) || null;
      }
    } catch (error) {
      console.error('SecureStorage getItem error:', error);
      return null;
    }
  }

  async removeItem(key: string): Promise<void> {
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        localStorage.removeItem(`secure_${key}`);
      } else {
        this.storage.delete(key);
      }
    } catch (error) {
      console.error('SecureStorage removeItem error:', error);
      throw error;
    }
  }

  async clear(): Promise<void> {
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        const keys = Object.keys(localStorage).filter(key => key.startsWith('secure_'));
        keys.forEach(key => localStorage.removeItem(key));
      } else {
        this.storage.clear();
      }
    } catch (error) {
      console.error('SecureStorage clear error:', error);
      throw error;
    }
  }

  async getAllKeys(): Promise<string[]> {
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        return Object.keys(localStorage)
          .filter(key => key.startsWith('secure_'))
          .map(key => key.replace('secure_', ''));
      } else {
        return Array.from(this.storage.keys());
      }
    } catch (error) {
      console.error('SecureStorage getAllKeys error:', error);
      return [];
    }
  }

  // Utility methods
  async setObject(key: string, value: any): Promise<void> {
    await this.setItem(key, JSON.stringify(value));
  }

  async getObject<T = any>(key: string): Promise<T | null> {
    const item = await this.getItem(key);
    if (!item) return null;
    
    try {
      return JSON.parse(item) as T;
    } catch (error) {
      console.error('SecureStorage getObject parse error:', error);
      return null;
    }
  }

  // Batch operations
  async setMultiple(keyValuePairs: Array<[string, string]>): Promise<void> {
    await Promise.all(
      keyValuePairs.map(([key, value]) => this.setItem(key, value))
    );
  }

  async getMultiple(keys: string[]): Promise<Array<[string, string | null]>> {
    const results = await Promise.all(
      keys.map(async (key) => [key, await this.getItem(key)] as [string, string | null])
    );
    return results;
  }

  async removeMultiple(keys: string[]): Promise<void> {
    await Promise.all(keys.map(key => this.removeItem(key)));
  }
}

// Export singleton instance
export const secureStorage = new MockSecureStorage();
export default secureStorage;

// Type exports
export type { SecureStorage };