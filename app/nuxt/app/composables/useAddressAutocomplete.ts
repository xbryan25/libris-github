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
  
    const addr = item.address || {};
    const parts: string[] = item.display_name.split(',').map(p => p.trim());
  
    address.latitude = parseFloat(item.lat);
    address.longitude = parseFloat(item.lon);
  
    // Street / road
    address.street = addr.road || addr.pedestrian || addr.footway || parts[0] || '';
  
    // Barangay (suburb/neighbourhood or 2nd part of display_name)
    address.barangay =
      addr.suburb ||
      addr.neighbourhood ||
      addr.quarter ||
      addr.hamlet ||
      parts[1] || '';
  
    // City / municipality
    address.city =
      addr.city ||
      addr.town ||
      addr.village ||
      addr.municipality ||
      parts[2] || '';
  
    // Province / state
    address.province = addr.state || parts[3] || '';
  
    // Postal code
    address.postal_code =
      addr.postcode || parts.find(p => /\d{4,6}/.test(p)) || '';
  
    // Country
    address.country = addr.country || parts[parts.length - 1] || '';
  
    addressQuery.value = item.display_name;
    suggestions.value = [];
  }
  
  return { addressQuery, suggestions, fetchSuggestions, selectSuggestion };
}
