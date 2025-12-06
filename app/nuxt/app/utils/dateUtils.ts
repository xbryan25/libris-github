export function dateConverter (dateStr: string, dateFormat: string): string {
  const date: Date = new Date(dateStr);

  if (dateFormat === 'short'){
    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
    });
  } else {
    const dateOptions: Intl.DateTimeFormatOptions = {
        weekday: 'short', // "Wed"
        month: 'short',   // "Nov"
        day: 'numeric',   // 19
    };

    // Options for toLocaleTimeString
    const timeOptions: Intl.DateTimeFormatOptions = {
        hour: 'numeric',
        minute: 'numeric',
        hour12: true,     // 6:49 PM
    };

    return `${date.toLocaleDateString('en-US', dateOptions)}, ${date.toLocaleTimeString('en-US', timeOptions)}`
  }
  
};

export function getDateDifference (dateStr: string): string {

    const today = new Date();
    const currentDate = new Date(dateStr);

    const diffMs = today.getTime() - currentDate.getTime()

    return formatDateDifference(diffMs);
}

function formatDateDifference (ms: number): string {
    const seconds = Math.floor(ms / 1000) % 60;
    const minutes = Math.floor(ms / (1000 * 60)) % 60;
    const hours = Math.floor(ms / (1000 * 60 * 60)) % 24;
    const days = Math.floor(ms / (1000 * 60 * 60 * 24));
    const weeks = Math.floor(ms / (1000 * 60 * 60 * 24 * 7))
    const months = Math.floor(ms / (1000 * 60 * 60 * 24 * 30))
    const years = Math.floor(ms / (1000 * 60 * 60 * 24 * 365))

    if (years == 1) return `${years} year ago`;
    if (years > 0) return `${years} years ago`;
    if (months == 1) return `${months} month ago`;
    if (months > 0) return `${months} month ago`;
    if (weeks == 1) return `${weeks} week ago`;
    if (weeks > 0) return `${weeks} week ago`;
    if (days == 1) return `${days} day ago`;
    if (days > 0) return `${days} days ago`;
    if (hours == 1) return `${hours} hour ago`;
    if (hours > 0) return `${hours} hours ago`;
    if (minutes == 1) return `${minutes} minute ago`;
    if (minutes > 0) return `${minutes} minutes ago`;
    if (seconds == 1) return `${seconds} second ago`;
    return `${seconds} seconds ago`;
}