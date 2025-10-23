import { ref } from 'vue'

export type TrustScoreComparison = {
    user_trust_score: number
    average_trust_score: number
    total_users: number
    percentage_difference: number
    is_above_average: boolean
}

const API_URL = import.meta.env.VITE_API_URL

export const useTrustScoreComparison = (userId?: string) => {
    const comparison = ref<TrustScoreComparison | null>(null)
    const loading = ref(false)
    const error = ref<string | null>(null)

    const fetchComparison = async () => {
        loading.value = true
        error.value = null
        try {
            // Use different endpoint based on whether we have a specific user ID
            const endpoint = userId
                ? `${API_URL}/api/users/trust-score-comparison/${userId}`
                : `${API_URL}/api/users/trust-score-comparison`

            console.log('Making API call to:', endpoint)
            const response = await fetch(endpoint, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                }
            })

            console.log('Response status:', response.status)

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`)
            }

            const res = await response.json()
            console.log('API response:', res)
            comparison.value = res
        } catch (e: any) {
            console.error('Trust score comparison error:', e)
            error.value = e?.message || 'Failed to fetch trust score comparison'
        } finally {
            loading.value = false
        }
    }

    const getComparisonText = () => {
        console.log('getComparisonText called, comparison.value:', comparison.value)
        if (!comparison.value) return 'Loading...'

        const { percentage_difference, is_above_average } = comparison.value
        const absPercentage = Math.abs(percentage_difference)

        console.log('percentage_difference:', percentage_difference, 'is_above_average:', is_above_average)

        const text = is_above_average
            ? `${Math.round(absPercentage)}% more than other people`
            : `${Math.round(absPercentage)}% less than other people`

        console.log('Returning text:', text)
        return text
    }

    return { comparison, loading, error, fetchComparison, getComparisonText }
}
