import type {FormError} from '@nuxt/ui';

export function validateAddEditBook (state: any): FormError[] {

	const titleAuthorRegex = /^[A-Za-z\s.'-]+$/;
	const numberRegex = /^[0-9]+$/;

	const whitespaceRegex = /^\s*$/;

	const errors: { name: string, message: string }[] = [];

	console.log(state.title)

	if (!state.title || whitespaceRegex.test(state.title)) {
			errors.push({ name: 'title', message: 'Title is required.' });
	} else if (state.title && !titleAuthorRegex.test(state.title)) {
			errors.push({
					name: 'title',
					message: 'Wrong title format.',
			});
	}

	if (!state.author || whitespaceRegex.test(state.author)) {
			errors.push({ name: 'author', message: 'Author is required.' });
	} else if (state.author && !titleAuthorRegex.test(state.author)) {
			errors.push({
					name: 'author',
					message: 'Wrong author format.',
			});
	}

	if (!state.dailyRentPrice || whitespaceRegex.test(state.dailyRentPrice)) {
			errors.push({ name: 'dailyRentPrice', message: 'Daily rent price is required.' });
	} else if (state.dailyRentPrice && !numberRegex.test(state.dailyRentPrice)) {
			errors.push({
					name: 'dailyRentPrice',
					message: 'Should only be numbers.',
			});
	}

	if (!state.securityDeposit || whitespaceRegex.test(state.securityDeposit)) {
			errors.push({ name: 'securityDeposit', message: 'Security deposit is required.' });
	} else if (state.securityDeposit && !numberRegex.test(state.securityDeposit)) {
			errors.push({
					name: 'securityDeposit',
					message: 'Should only be numbers.',
			});
	}

	if (!state.purchasePrice || whitespaceRegex.test(state.purchasePrice)) {
			errors.push({ name: 'purchasePrice', message: 'Purchase price is required.' });
	} else if (state.purchasePrice && !numberRegex.test(state.purchasePrice)) {
			errors.push({
					name: 'purchasePrice',
					message: 'Should only be numbers.',
			});
	}
    
	return errors;
};