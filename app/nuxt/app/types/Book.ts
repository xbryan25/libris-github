
export interface Book {
    bookId: string
    title: string
    author: string
    genre: string
    condition: string
    description: string
    availability: string
    dailyRentPrice: number
    securityDeposit: number
    purchasePrice: number
    ownerId: string
    ownerUsername: string
    firstImageUrl: string | null
};