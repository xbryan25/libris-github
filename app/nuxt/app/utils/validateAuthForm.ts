import type {FormError} from '@nuxt/ui';

export function validateAuthForm (state: any, authType: string): FormError[] {

    const emailAddressRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; 
    const passwordRegex = /^.{8,}$/;

    const whitespaceRegex = /^\s*$/;

    const errors: { name: string, message: string }[] = [];

    if (authType === 'login'){
        if (!state.emailAddress || whitespaceRegex.test(state.emailAddress)) {
            errors.push({ name: 'emailAddress', message: 'Email address is required.' });
        } else if (state.emailAddress && !emailAddressRegex.test(state.emailAddress)) {
            errors.push({
                name: 'emailAddress',
                message: 'Wrong email address format.',
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

    if (authType === 'signup'){
        if (!state.username || whitespaceRegex.test(state.username)) {
            errors.push({ name: 'username', message: 'Username is required.' });
        }

        if (!state.emailAddress || whitespaceRegex.test(state.emailAddress)) {
            errors.push({ name: 'emailAddress', message: 'Email address is required.' });
        } else if (state.emailAddress && !emailAddressRegex.test(state.emailAddress)) {
            errors.push({
                name: 'emailAddress',
                message: 'Wrong email address format.',
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

        if (!state.confirmPassword || whitespaceRegex.test(state.confirmPassword)) {
            errors.push({ name: 'confirmPassword', message: 'Confirm password is required.' });
        } else if (state.password !== state.confirmPassword) {
            errors.push({
                name: 'confirmPassword',
                message: 'Passwords do not match.',
            });
        }
    }

    return errors;
}