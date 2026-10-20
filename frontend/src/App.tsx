import {
  useEffect,
  useState,
  type FormEvent,
} from "react"

import {
  createExpense,
  createGroup,
  createMember,
  getBalances,
  getExpenses,
  getGroups,
  getMembers,
  getSettlements,
  type Balance,
  type Expense,
  type Group,
  type Member,
  type Settlement,
} from "./services/api"


async function fetchGroupData(groupId: number) {
  const [
    members,
    balances,
    settlements,
    expenses,
  ] = await Promise.all([
    getMembers(groupId),
    getBalances(groupId),
    getSettlements(groupId),
    getExpenses(groupId),
  ])

  return {
    members,
    balances,
    settlements,
    expenses,
  }
}


function formatMoney(cents: number) {
  return `${(Math.abs(cents) / 100).toFixed(2)} KM`
}


function App() {
  const [groups, setGroups] = useState<Group[]>([])

  const [selectedGroup, setSelectedGroup] =
    useState<Group | null>(null)

  const [members, setMembers] = useState<Member[]>([])
  const [balances, setBalances] = useState<Balance[]>([])
  const [settlements, setSettlements] =
    useState<Settlement[]>([])
  const [expenses, setExpenses] = useState<Expense[]>([])

  const [description, setDescription] = useState("")
  const [amount, setAmount] = useState("")
  const [payerMemberId, setPayerMemberId] =
    useState("")

  const [showMemberForm, setShowMemberForm] =
    useState(false)

  const [newMemberName, setNewMemberName] =
    useState("")

  const [showGroupForm, setShowGroupForm] =
    useState(false)

  const [newGroupName, setNewGroupName] =
    useState("")

  const [loading, setLoading] = useState(true)

  const [submittingExpense, setSubmittingExpense] =
    useState(false)

  const [submittingMember, setSubmittingMember] =
    useState(false)

  const [submittingGroup, setSubmittingGroup] =
    useState(false)

  const [error, setError] = useState("")


  function applyGroupData(data: {
    members: Member[]
    balances: Balance[]
    settlements: Settlement[]
    expenses: Expense[]
  }) {
    setMembers(data.members)
    setBalances(data.balances)
    setSettlements(data.settlements)
    setExpenses(data.expenses)

    setPayerMemberId(
      data.members.length > 0
        ? String(data.members[0].id)
        : "",
    )
  }


  useEffect(() => {
    async function loadInitialData() {
      try {
        setError("")

        const loadedGroups = await getGroups()

        setGroups(loadedGroups)

        if (loadedGroups.length > 0) {
          const firstGroup = loadedGroups[0]

          setSelectedGroup(firstGroup)

          const data = await fetchGroupData(
            firstGroup.id,
          )

          applyGroupData(data)
        }
      } catch {
        setError(
          "Failed to load SplitLedger data.",
        )
      } finally {
        setLoading(false)
      }
    }

    loadInitialData()
  }, [])


  async function handleGroupSelect(group: Group) {
    try {
      setError("")
      setSelectedGroup(group)

      const data = await fetchGroupData(group.id)

      applyGroupData(data)

      setDescription("")
      setAmount("")
      setNewMemberName("")
      setShowMemberForm(false)
    } catch {
      setError(
        "Failed to load group data.",
      )
    }
  }


  async function handleExpenseSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault()

    if (!selectedGroup) {
      setError("Select a group first.")
      return
    }

    if (!payerMemberId) {
      setError(
        "Add at least one member before creating an expense.",
      )
      return
    }

    try {
      setError("")
      setSubmittingExpense(true)

      await createExpense(
        selectedGroup.id,
        {
          payer_member_id:
            Number(payerMemberId),
          description,
          amount,
        },
      )

      const data = await fetchGroupData(
        selectedGroup.id,
      )

      applyGroupData(data)

      setDescription("")
      setAmount("")
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message)
      } else {
        setError(
          "Failed to create expense.",
        )
      }
    } finally {
      setSubmittingExpense(false)
    }
  }


  async function handleMemberSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault()

    if (!selectedGroup) {
      setError("Select a group first.")
      return
    }

    try {
      setError("")
      setSubmittingMember(true)

      await createMember(
        selectedGroup.id,
        {
          name: newMemberName,
        },
      )

      const data = await fetchGroupData(
        selectedGroup.id,
      )

      applyGroupData(data)

      setNewMemberName("")
      setShowMemberForm(false)
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message)
      } else {
        setError(
          "Failed to add member.",
        )
      }
    } finally {
      setSubmittingMember(false)
    }
  }


  async function handleGroupSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault()

    try {
      setError("")
      setSubmittingGroup(true)

      const createdGroup = await createGroup(
        newGroupName,
      )

      const loadedGroups = await getGroups()

      setGroups(loadedGroups)

      const group =
        loadedGroups.find(
          (item) =>
            item.id === createdGroup.id,
        ) ?? null

      if (group) {
        setSelectedGroup(group)

        const data = await fetchGroupData(
          group.id,
        )

        applyGroupData(data)
      }

      setNewGroupName("")
      setShowGroupForm(false)
      setShowMemberForm(false)
      setDescription("")
      setAmount("")
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message)
      } else {
        setError(
          "Failed to create group.",
        )
      }
    } finally {
      setSubmittingGroup(false)
    }
  }


  if (loading) {
    return (
      <main className="workspace">
        <p>Loading SplitLedger...</p>
      </main>
    )
  }


  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div>
          <div className="brand">
            <div className="brand-mark">
              S
            </div>

            <div>
              <h1>SplitLedger</h1>
              <p>Expense sharing</p>
            </div>
          </div>

          <div className="sidebar-section">
            <span className="section-label">
              GROUPS
            </span>

            {groups.length > 0 ? (
              groups.map((group) => (
                <button
                  key={group.id}
                  className={
                    selectedGroup?.id ===
                    group.id
                      ? "group-button active"
                      : "group-button"
                  }
                  onClick={() =>
                    handleGroupSelect(group)
                  }
                >
                  {group.name}
                </button>
              ))
            ) : (
              <p className="muted">
                No groups yet.
              </p>
            )}
          </div>
        </div>

        <div className="new-group-area">
          {showGroupForm && (
            <form
              className="group-form"
              onSubmit={handleGroupSubmit}
            >
              <input
                type="text"
                placeholder="Group name"
                value={newGroupName}
                onChange={(event) =>
                  setNewGroupName(
                    event.target.value,
                  )
                }
                autoFocus
              />

              <button
                type="submit"
                disabled={submittingGroup}
              >
                {submittingGroup
                  ? "Creating..."
                  : "Create"}
              </button>
            </form>
          )}

          <button
            className="new-group-button"
            onClick={() =>
              setShowGroupForm(
                !showGroupForm,
              )
            }
          >
            {showGroupForm
              ? "Cancel"
              : "+ New group"}
          </button>
        </div>
      </aside>

      <main className="workspace">
        {error && (
          <div className="card">
            <strong>{error}</strong>
          </div>
        )}

        <header className="workspace-header">
          <div>
            <p className="eyebrow">
              GROUP
            </p>

            <h2>
              {selectedGroup?.name ??
                "No group selected"}
            </h2>

            <p className="muted">
              Track shared expenses and
              settle balances.
            </p>
          </div>

          <span className="currency-badge">
            BAM
          </span>
        </header>

        <section className="card">
          <div className="section-header">
            <div>
              <h3>Members</h3>

              <p>
                {members.length}{" "}
                {members.length === 1
                  ? "person"
                  : "people"}{" "}
                in this group
              </p>
            </div>

            <button
              className="secondary-button"
              onClick={() =>
                setShowMemberForm(
                  !showMemberForm,
                )
              }
              disabled={!selectedGroup}
            >
              {showMemberForm
                ? "Cancel"
                : "+ Add member"}
            </button>
          </div>

          {showMemberForm && (
            <form
              className="member-form"
              onSubmit={handleMemberSubmit}
            >
              <input
                type="text"
                placeholder="Member name"
                value={newMemberName}
                onChange={(event) =>
                  setNewMemberName(
                    event.target.value,
                  )
                }
                autoFocus
              />

              <button
                className="primary-button"
                type="submit"
                disabled={submittingMember}
              >
                {submittingMember
                  ? "Adding..."
                  : "Add"}
              </button>
            </form>
          )}

          <div className="member-list">
            {members.length > 0 ? (
              members.map((member) => (
                <span key={member.id}>
                  {member.name}
                </span>
              ))
            ) : (
              <p className="muted">
                No members yet.
              </p>
            )}
          </div>
        </section>

        <div className="dashboard-grid">
          <section className="card">
            <div className="section-header">
              <div>
                <h3>Add expense</h3>

                <p>
                  Record a shared group
                  expense
                </p>
              </div>
            </div>

            <form
              className="expense-form"
              onSubmit={handleExpenseSubmit}
            >
              <label>
                Description

                <input
                  type="text"
                  placeholder="Apartment"
                  value={description}
                  onChange={(event) =>
                    setDescription(
                      event.target.value,
                    )
                  }
                />
              </label>

              <label>
                Amount

                <input
                  type="text"
                  placeholder="100.00"
                  value={amount}
                  onChange={(event) =>
                    setAmount(
                      event.target.value,
                    )
                  }
                />
              </label>

              <label>
                Paid by

                <select
                  value={payerMemberId}
                  onChange={(event) =>
                    setPayerMemberId(
                      event.target.value,
                    )
                  }
                  disabled={
                    members.length === 0
                  }
                >
                  {members.length === 0 && (
                    <option value="">
                      No members available
                    </option>
                  )}

                  {members.map(
                    (member) => (
                      <option
                        key={member.id}
                        value={member.id}
                      >
                        {member.name}
                      </option>
                    ),
                  )}
                </select>
              </label>

              <button
                className="primary-button"
                type="submit"
                disabled={
                  !selectedGroup ||
                  members.length === 0 ||
                  submittingExpense
                }
              >
                {submittingExpense
                  ? "Adding..."
                  : "Add expense"}
              </button>
            </form>
          </section>

          <section className="card">
            <div className="section-header">
              <div>
                <h3>Balances</h3>

                <p>
                  Current net position
                </p>
              </div>
            </div>

            <div className="balance-list">
              {balances.length > 0 ? (
                balances.map(
                  (balance) => (
                    <div
                      className="balance-row"
                      key={
                        balance.member_id
                      }
                    >
                      <span>
                        {
                          balance.member_name
                        }
                      </span>

                      <strong
                        className={
                          balance.balance_cents >
                          0
                            ? "positive"
                            : balance.balance_cents <
                                0
                              ? "negative"
                              : ""
                        }
                      >
                        {balance.balance_cents >
                        0
                          ? "+"
                          : balance.balance_cents <
                              0
                            ? "-"
                            : ""}

                        {formatMoney(
                          balance.balance_cents,
                        )}
                      </strong>
                    </div>
                  ),
                )
              ) : (
                <p className="muted">
                  No balances yet.
                </p>
              )}
            </div>
          </section>
        </div>

        <div className="dashboard-grid">
          <section className="card">
            <div className="section-header">
              <div>
                <h3>Expenses</h3>

                <p>
                  Recent group activity
                </p>
              </div>
            </div>

            {expenses.length > 0 ? (
              expenses.map((expense) => (
                <div
                  className="expense-row"
                  key={expense.id}
                >
                  <div>
                    <strong>
                      {expense.description}
                    </strong>

                    <p>
                      Paid by{" "}
                      {expense.payer_name}
                    </p>
                  </div>

                  <strong>
                    {formatMoney(
                      expense.amount_cents,
                    )}
                  </strong>
                </div>
              ))
            ) : (
              <p className="muted">
                No expenses yet.
              </p>
            )}
          </section>

          <section className="card">
            <div className="section-header">
              <div>
                <h3>
                  Suggested settlements
                </h3>

                <p>
                  How to settle the group
                </p>
              </div>
            </div>

            <div className="settlement-list">
              {settlements.length > 0 ? (
                settlements.map(
                  (
                    settlement,
                    index,
                  ) => (
                    <div
                      className="settlement-row"
                      key={`${settlement.from_member_id}-${settlement.to_member_id}-${index}`}
                    >
                      <span>
                        {
                          settlement.from_member_name
                        }
                        {" → "}
                        {
                          settlement.to_member_name
                        }
                      </span>

                      <strong>
                        {formatMoney(
                          settlement.amount_cents,
                        )}
                      </strong>
                    </div>
                  ),
                )
              ) : (
                <p className="muted">
                  Everyone is settled up.
                </p>
              )}
            </div>
          </section>
        </div>
      </main>
    </div>
  )
}

export default App