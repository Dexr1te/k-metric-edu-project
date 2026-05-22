import { describe, it, expect, beforeEach } from 'vitest';
import { useAuthStore } from '../store/authStore';

describe('AuthStore (Zustand)', () => {
  beforeEach(() => {
    // Очищаем состояние перед каждым тестом
    useAuthStore.getState().logout();
  });

  it('EDU: Начальное состояние должно быть неавторизованным', () => {
    const state = useAuthStore.getState();
    expect(state.isAuthenticated).toBe(false);
    expect(state.token).toBe(null);
  });

  it('EDU: Метод login должен устанавливать токен и статус', () => {
    const testToken = 'fake-jwt-token';
    useAuthStore.getState().login(testToken);
    
    const state = useAuthStore.getState();
    expect(state.isAuthenticated).toBe(true);
    expect(state.token).toBe(testToken);
  });

  it('EDU: Метод logout должен очищать состояние', () => {
    useAuthStore.getState().login('token');
    useAuthStore.getState().logout();
    
    const state = useAuthStore.getState();
    expect(state.isAuthenticated).toBe(false);
    expect(state.token).toBe(null);
  });
});
