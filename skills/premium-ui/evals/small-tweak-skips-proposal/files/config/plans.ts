export const plans = [
  { id: 'baslangic', name: 'Başlangıç', monthlyPrice: 249, yearlyPrice: 2490, stores: 1, ordersPerMonth: 500, sms: false },
  { id: 'profesyonel', name: 'Profesyonel', monthlyPrice: 599, yearlyPrice: 5990, stores: 3, ordersPerMonth: 3000, sms: true },
  { id: 'kurumsal', name: 'Kurumsal', monthlyPrice: 1490, yearlyPrice: 14900, stores: 10, ordersPerMonth: 20000, sms: true },
] as const
