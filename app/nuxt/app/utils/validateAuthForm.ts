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
        } else if (state.username && state.username.length < 3) {
            errors.push({
                name: 'username',
                message: 'Username must be at least 3 characters long.',
            });
        } else if (state.username && state.username.length > 64) {
            errors.push({
                name: 'username',
                message: 'Username must not exceed 64 characters.',
            });
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
        } else if (state.password && state.password.length > 64) {
            errors.push({
                name: 'password',
                message: 'Password must not exceed 64 characters.',
            });
        }
        // REMOVED: Strong password validation from here
        // The PasswordStrengthMeter component and backend will handle it

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


export function validateNewUsername (newUsername: string, isOpenAddUsernameModal: boolean): FormError[] {

    const whitespaceRegex = /^\s*$/;

    const errors: { name: string, message: string }[] = [];

    if (!isOpenAddUsernameModal){
        return errors
    }

    if (!newUsername || whitespaceRegex.test(newUsername)) {
        errors.push({ name: 'username', message: 'Username is required.' });
    } else if (newUsername && newUsername.length < 3) {
        errors.push({
            name: 'username',
            message: 'Username must be at least 3 characters long.',
        });
    } else if (newUsername && newUsername.length > 64) {
        errors.push({
            name: 'username',
            message: 'Username must not exceed 64 characters.',
        });
    }

    return errors;
}