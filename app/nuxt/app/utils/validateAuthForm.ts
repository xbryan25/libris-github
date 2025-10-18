import type {FormError} from '@nuxt/ui';

export function validateAuthForm (state: any, authType: string): FormError[] {

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const passwordRegex = /^.{8,}$/;

    const whitespaceRegex = /^\s*$/;

    const errors: { name: string, message: string }[] = [];

    if (authType === 'login'){
        if (!state.email || whitespaceRegex.test(state.email)) {
            errors.push({ name: 'email', message: 'Email is required.' });
        } else if (state.email && !emailRegex.test(state.email)) {
            errors.push({
                name: 'email',
                message: 'Wrong email format.',
            });
        }

        if (!state.password || whitespaceRegex.test(state.password)) {
            errors.push({ name: 'password', message: 'Password is required.' });
        } else if (state.password && !passwordRegex.test(state.password)) {
            errors.push({
                name: 'password',
                message: 'Passwords should be at least 8 characters long.',
            });
        }
    }

    return errors;
};