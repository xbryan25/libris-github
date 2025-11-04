import type {FormError} from '@nuxt/ui';

export function validateAddEditBook (state: any, formType: string): FormError[] {

	const titleAuthorRegex = /^[A-Za-z\s.'-]+$/;
	const numberRegex = /^[0-9]+$/;

	const whitespaceRegex = /^\s*$/;

	const errors: { name: string, message: string }[] = [];

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

	if (!state.genres || state.genres.length == 0){
		errors.push({ name: 'genres', message: 'At least one genre is required.' });
	}

	if (!state.condition || whitespaceRegex.test(state.condition)) {
			errors.push({ name: 'condition', message: 'Condition is required.' });
	}

	if (formType === 'add' && (!state.bookImages || state.bookImages.length == 0)){
		errors.push({ name: 'bookImages', message: 'At least one image is required.' });
	} else if (formType === 'edit' && (state.existingBookImageUrls.length == 0 && state.bookImages.length == 0)){
		errors.push({ name: 'bookImages', message: 'At least one image is required.' });
	}
	
	if (!state.description || whitespaceRegex.test(state.description)){
		errors.push({ name: 'description', message: 'A short description is required.' });
	}

	if (!state.availability || whitespaceRegex.test(state.availability)) {
		errors.push({ name: 'availability', message: 'Availability is required.' });
	} else {
		if (state.availability == 'For Sale' || state.availability == 'Both'){
			if (!state.purchasePrice || whitespaceRegex.test(state.purchasePrice)) {
				errors.push({ name: 'purchasePrice', message: 'Purchase price is required.' });
	} else if (state.purchasePrice && !numberRegex.test(state.purchasePrice)) {
					errors.push({
							name: 'purchasePrice',
							message: 'Should only be numbers.',
					});
			}
		}

	if (state.availability == 'For Rent' || state.availability == 'Both'){
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
		}
	}

	return errors;
};