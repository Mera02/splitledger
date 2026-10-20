const API_URL = "http://127.0.0.1:8000/api"


export type Group = {
  id: number
  name: string
  created_at: string
}


export type Member = {
  id: number
  group_id: number
  name: string
  created_at: string
}

export type CreateMemberInput = {
  name: string
}

export type Balance = {
  member_id: number
  member_name: string
  balance_cents: number
}


export type Settlement = {
  from_member_id: number
  from_member_name: string
  to_member_id: number
  to_member_name: string
  amount_cents: number
}


export type Expense = {
  id: number
  group_id: number
  payer_member_id: number
  payer_name: string
  description: string
  amount_cents: number
  created_at: string
}


export type CreateExpenseInput = {
  payer_member_id: number
  description: string
  amount: string
}


export async function getGroups(): Promise<Group[]> {
  const response = await fetch(
    `${API_URL}/groups`,
  )

  if (!response.ok) {
    throw new Error("Failed to load groups.")
  }

  return response.json()
}


export async function getMembers(
  groupId: number,
): Promise<Member[]> {
  const response = await fetch(
    `${API_URL}/groups/${groupId}/members`,
  )

  if (!response.ok) {
    throw new Error("Failed to load members.")
  }

  return response.json()
}


export async function getBalances(
  groupId: number,
): Promise<Balance[]> {
  const response = await fetch(
    `${API_URL}/groups/${groupId}/balances`,
  )

  if (!response.ok) {
    throw new Error("Failed to load balances.")
  }

  return response.json()
}


export async function getSettlements(
  groupId: number,
): Promise<Settlement[]> {
  const response = await fetch(
    `${API_URL}/groups/${groupId}/settlements`,
  )

  if (!response.ok) {
    throw new Error("Failed to load settlements.")
  }

  return response.json()
}


export async function getExpenses(
  groupId: number,
): Promise<Expense[]> {
  const response = await fetch(
    `${API_URL}/groups/${groupId}/expenses`,
  )

  if (!response.ok) {
    throw new Error("Failed to load expenses.")
  }

  return response.json()
}


export async function createExpense(
  groupId: number,
  expense: CreateExpenseInput,
) {
  const response = await fetch(
    `${API_URL}/groups/${groupId}/expenses`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(expense),
    },
  )

  if (!response.ok) {
    const errorData = await response.json()

    throw new Error(
      errorData.detail ?? "Failed to create expense.",
    )
  }

  return response.json()
}

export async function createMember(
  groupId: number,
  member: CreateMemberInput,
) {
  const response = await fetch(
    `${API_URL}/groups/${groupId}/members`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(member),
    },
  )

  if (!response.ok) {
    const errorData = await response.json()

    throw new Error(
      errorData.detail ?? "Failed to add member.",
    )
  }

  return response.json()
}


export async function createGroup(name: string) {
  const response = await fetch(
    `${API_URL}/groups`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name,
      }),
    },
  )

  if (!response.ok) {
    const errorData = await response.json()

    throw new Error(
      errorData.detail ?? "Failed to create group.",
    )
  }

  return response.json()
}