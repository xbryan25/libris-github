import type { FormError } from '@nuxt/ui'

export function validateProfileForm(state: any): FormError[] {
  // Improved regex patterns
  const nameRegex = /^[A-Za-z]+(?:\s+[A-Za-z]+)*$/ // Allows letters and spaces, but no leading/trailing spaces or consecutive spaces
  const countryRegex = /^[A-Za-z\s]+$/ // Allows letters and spaces for country names
  const phoneRegex = /^[0-9]{11}$/
  const whitespaceRegex = /^\s*$/

  const errors: FormError[] = []

  // First name validation
  if (!state.first_name || whitespaceRegex.test(state.first_name)) {
    errors.push({ name: 'first_name', message: 'First name is required.' })
  } else if (!nameRegex.test(state.first_name.trim())) {
    errors.push({ name: 'first_name', message: 'First name must contain only letters and spaces.' })
  }

  // Middle name validation (optional)
  if (state.middle_name && !whitespaceRegex.test(state.middle_name) && !nameRegex.test(state.middle_name.trim())) {
    errors.push({ name: 'middle_name', message: 'Middle name must contain only letters and spaces.' })
  }

  // Last name validation
  if (!state.last_name || whitespaceRegex.test(state.last_name)) {
    errors.push({ name: 'last_name', message: 'Last name is required.' })
  } else if (!nameRegex.test(state.last_name.trim())) {
    errors.push({ name: 'last_name', message: 'Last name must contain only letters and spaces.' })
  }

  // Phone number validation
  if (state.phone_number && !whitespaceRegex.test(state.phone_number)) {
    const phoneValue = state.phone_number.trim()

    // Check if contains non-numeric characters
    if (!/^[0-9]+$/.test(phoneValue)) {
      errors.push({ name: 'phone_number', message: 'Phone number must contain only numbers.' })
    }
    // Check if not exactly 11 digits
    else if (phoneValue.length !== 11) {
      errors.push({ name: 'phone_number', message: 'Phone number must be exactly 11 digits.' })
    }
  }

  // Country validation
  if (state.address?.country && !whitespaceRegex.test(state.address.country) && !countryRegex.test(state.address.country.trim())) {
    errors.push({ name: 'address.country', message: 'Country must contain only letters and spaces.' })
  }

  return errors
}
