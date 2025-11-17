import { ref } from 'vue';

export function useAddressAutocomplete(apiKey: string) {
  const query = ref('');
  const suggestions = ref<any[]>([]);

  async function fetchSuggestions() {
    if (!query.value) {
      suggestions.value = [];
      return;
    }
    try {
      const res = await fetch(
        `https://us1.locationiq.com/v1/search.php?key=${apiKey}&q=${encodeURIComponent(
          query.value
        )}&format=json&limit=5`
      );
      if (!res.ok) throw new Error('Network response was not ok');
      const data = await res.json();
      suggestions.value = data;
    } catch (err) {
      console.error('Fetch error:', err);
      suggestions.value = [];
    }
  }

  function selectSuggestion(item: any, address: any) {
    if (!address) return;
    address.street = item.address?.road || item.display_name.split(',')[1]?.trim() || '';
    address.city = item.address?.city || item.address?.town || item.address?.village || '';
    address.postal_code = item.address?.postcode || '';
    address.country = item.address?.country || '';
    address.latitude = parseFloat(item.lat);
    address.longitude = parseFloat(item.lon);
    query.value = item.display_name;
    suggestions.value = [];
  }

  return { query, suggestions, fetchSuggestions, selectSuggestion };
}
