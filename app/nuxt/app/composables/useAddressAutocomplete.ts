import { ref, watch } from 'vue';
import { debounce } from 'lodash';

export function useAddressAutocomplete(apiKey: string) {
  const addressQuery = ref('');
  const suggestions = ref<any[]>([]);

  const fetchSuggestions = async () => {
    if (!addressQuery.value) {
      suggestions.value = [];
      return;
    }
    try {
      const res = await fetch(
        `https://api.locationiq.com/v1/autocomplete.php?key=${apiKey}&q=${encodeURIComponent(addressQuery.value)}&limit=5&dedupe=1`
      );
      if (!res.ok) throw new Error('Network response was not ok');
      suggestions.value = await res.json();
    } catch (err) {
      console.error('Fetch error:', err);
      suggestions.value = [];
    }
  };

  const debouncedFetch = debounce(fetchSuggestions, 500); 

  watch(addressQuery, (val) => {
    if (!val) {
      suggestions.value = [];
      return;
    }
    debouncedFetch();
  });

  function selectSuggestion(item: any, address: any) {
    if (!address) return;
    address.street = item.address?.road || item.display_name.split(',')[0]?.trim() || '';
    address.city = item.address?.city || item.address?.town || item.address?.village || '';
    address.postal_code = item.address?.postcode || '';
    address.country = item.address?.country || '';
    address.latitude = parseFloat(item.lat);
    address.longitude = parseFloat(item.lon);
    addressQuery.value = item.display_name;
    suggestions.value = [];
  }

  return { addressQuery, suggestions, selectSuggestion };
}
