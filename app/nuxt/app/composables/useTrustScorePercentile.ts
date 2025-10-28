import { ref } from 'vue'

export type TrustScorePercentile = {
    user_id: string
    trust_score_percentile: number
    is_above_average: boolean
}

const API_URL = import.meta.env.VITE_API_URL

export const useTrustScorePercentile = (userId?: string) => {
    const percentile = ref<TrustScorePercentile | null>(null)
    const loading = ref(false)
    const error = ref<string | null>(null)

    const fetchPercentile = async () => {
        loading.value = true
        error.value = null
        try {
            const endpoint = userId
                ? `${API_URL}/api/users/trust-score-percentile/${userId}`
                : `${API_URL}/api/users/trust-score-percentile`

            console.log('Making API call to:', endpoint)
            const response = await fetch(endpoint, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                }
            })

            console.log('Response status:', response.status)
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)

            const res = await response.json()
            console.log('API response:', res)
            percentile.value = res
        } catch (e: any) {
            console.error('Trust score percentile error:', e)
            error.value = e?.message || 'Failed to fetch trust score percentile'
        } finally {
            loading.value = false
        }
    }

    const getPercentileText = () => {
        const p = percentile.value?.trust_score_percentile
        if (p === null || p === undefined) return ' - '
        const rounded = Math.round(p)
        return `Better than ${rounded}% of users`
      }
    return { percentile, loading, error, fetchPercentile, getPercentileText }
}
