import React from 'react'
import { useMemo, useState } from 'react'
import './App.css'

const DEFAULT_BASE_URL = 'http://localhost:8000'
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || DEFAULT_BASE_URL

const ROLE_CONFIG = {
  customer: {
    title: 'Customer Portal',
    splash: 'Personal Banking',
  },
  admin: {
    title: 'Admin Portal',
    splash: 'Operations Command',
  },
}

const emptyAuthForm = {
  name: '',
  password: '',
  register_token: '',
  account_type: 'savings',
  balance: '0',
}

function App() {
  const [activePortal, setActivePortal] = useState('customer')
  const [authView, setAuthView] = useState({ customer: 'login', admin: 'login' })
  const [forms, setForms] = useState({ customer: emptyAuthForm, admin: emptyAuthForm })
  const [sessions, setSessions] = useState({ customer: null, admin: null })
  const [nameUpdate, setNameUpdate] = useState({ customer: '', admin: '' })
  const [passwordUpdate, setPasswordUpdate] = useState({ customer: '', admin: '' })
  const [balanceDelta, setBalanceDelta] = useState({ customer: '0', admin: '0' })
  const [adminCustomers, setAdminCustomers] = useState([])
  const [adminAdmins, setAdminAdmins] = useState([])
  const [loading, setLoading] = useState(false)
  const [notice, setNotice] = useState({ type: '', text: '' })
  const [sortColumn, setSortColumn] = useState('id')
  const [sortOrder, setSortOrder] = useState('asc')
  const [showPremiumOnly, setShowPremiumOnly] = useState(false)

  const session = sessions[activePortal]
  const roleLabel = ROLE_CONFIG[activePortal]
  const isRegisterMode = authView[activePortal] === 'register'

  const resolveUrl = (path) => `${BACKEND_URL.trim().replace(/\/$/, '')}${path}`

  const getApiPathCandidates = (path) => {
    return [path]
  }

  const setRoleSession = (role, data) => {
    setSessions((prev) => ({ ...prev, [role]: data }))
  }

  const withNotice = async (work) => {
    try {
      setLoading(true)
      setNotice({ type: '', text: '' })
      await work()
    } catch (error) {
      setNotice({ type: 'error', text: error.message || 'Request failed.' })
    } finally {
      setLoading(false)
    }
  }

  const apiRequest = async (path, options = {}) => {
    const pathCandidates = getApiPathCandidates(path)
    let lastError = null

    for (let i = 0; i < pathCandidates.length; i += 1) {
      const response = await fetch(resolveUrl(pathCandidates[i]), {
        method: options.method || 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...(options.token ? { Authorization: `Bearer ${options.token}` } : {}),
        },
        body: options.body ? JSON.stringify(options.body) : undefined,
      })

      if (response.status === 204) return null

      const data = await response.json().catch(() => null)
      if (response.ok) {
        return data
      }
      lastError = new Error(data?.detail || `Request failed (${response.status})`)
    }

    throw lastError || new Error('Request failed')
  }

  const updateForm = (role, key, value) => {
    setForms((prev) => ({
      ...prev,
      [role]: { ...prev[role], [key]: value },
    }))
  }

  const toggleAuthView = () => {
    setAuthView((prev) => ({
      ...prev,
      [activePortal]: prev[activePortal] === 'register' ? 'login' : 'register',
    }))
  }

  const register = async (role) => {
    const form = forms[role]
    await withNotice(async () => {
      const payload = role === 'customer'
        ? {
            name: form.name.trim(),
            password: form.password,
            register_token: form.register_token.trim(),
            account_type: form.account_type,
            balance: Number(form.balance),
          }
        : {
            name: form.name.trim(),
            password: form.password,
            register_token: form.register_token.trim(),
          }

      if (!payload.name || !payload.password || !payload.register_token) {
        throw new Error('Name, password, and register token are required.')
      }

      const data = await apiRequest(`/api/auth/register/${role}`, {
        method: 'POST',
        body: payload,
      })

      setRoleSession(role, data)
      setNameUpdate((prev) => ({ ...prev, [role]: data.profile.user.name }))
      setNotice({ type: 'success', text: `${roleLabel.title} registered and logged in.` })

      if (role === 'admin') {
        await refreshAdminTables(data.token)
      }
    })
  }

  const login = async (role) => {
    const form = forms[role]
    await withNotice(async () => {
      const payload = { name: form.name.trim(), password: form.password }
      if (!payload.name || !payload.password) {
        throw new Error('Name and password are required.')
      }

      const data = await apiRequest(`/api/auth/login/${role}`, {
        method: 'POST',
        body: payload,
      })

      setRoleSession(role, data)
      setNameUpdate((prev) => ({ ...prev, [role]: data.profile.user.name }))
      setNotice({ type: 'success', text: `Welcome back, ${data.profile.user.name}.` })

      if (role === 'admin') {
        await refreshAdminTables(data.token)
      }
    })
  }

  const refreshMe = async (role, token = sessions[role]?.token) => {
    if (!token) return
    const profile = await apiRequest('/api/auth/me', { token })
    setRoleSession(role, { token, profile })
    if (role === 'admin') {
      await refreshAdminTables(token)
    }
  }

  const logout = async (role) => {
    const token = sessions[role]?.token
    await withNotice(async () => {
      if (token) {
        await apiRequest('/api/auth/logout', { method: 'POST', token })
      }
      setRoleSession(role, null)
      if (role === 'admin') {
        setAdminCustomers([])
        setAdminAdmins([])
      }
      setNotice({ type: 'success', text: `${ROLE_CONFIG[role].title} logged out.` })
    })
  }

  const submitNameUpdate = async () => {
    const token = session?.token
    const nextName = nameUpdate[activePortal].trim()
    await withNotice(async () => {
      if (!token) throw new Error('Login required.')
      if (!nextName) throw new Error('Name is required.')

      const profile = await apiRequest('/api/auth/me/name', {
        method: 'PATCH',
        token,
        body: { name: nextName },
      })
      setRoleSession(activePortal, { token, profile })
      setNotice({ type: 'success', text: 'Name updated.' })
      if (activePortal === 'admin') {
        await refreshAdminTables(token)
      }
    })
  }

  const submitPasswordUpdate = async () => {
    const token = session?.token
    const password = passwordUpdate[activePortal]
    await withNotice(async () => {
      if (!token) throw new Error('Login required.')
      if (!password) throw new Error('Password is required.')

      await apiRequest('/api/auth/me/password', {
        method: 'PATCH',
        token,
        body: { password },
      })
      setPasswordUpdate((prev) => ({ ...prev, [activePortal]: '' }))
      setNotice({ type: 'success', text: 'Password updated.' })
    })
  }

  const adjustBalance = async (sign) => {
    const token = session?.token
    const amount = Number(balanceDelta[activePortal])

    await withNotice(async () => {
      if (!token) throw new Error('Login required.')
      if (Number.isNaN(amount) || amount <= 0) {
        throw new Error('Enter a positive amount.')
      }

      const profile = await apiRequest('/api/auth/me/balance/adjust', {
        method: 'POST',
        token,
        body: { amount: sign * amount },
      })
      setRoleSession(activePortal, { token, profile })
      setNotice({
        type: 'success',
        text: `${sign > 0 ? 'Added' : 'Subtracted'} $${amount.toFixed(2)} successfully.`,
      })
      if (activePortal === 'admin') {
        await refreshAdminTables(token)
      }
    })
  }

  const deleteSelf = async () => {
    const token = session?.token
    await withNotice(async () => {
      if (!token) throw new Error('Login required.')

      await apiRequest('/api/auth/me', { method: 'DELETE', token })
      setRoleSession(activePortal, null)
      if (activePortal === 'admin') {
        setAdminCustomers([])
        setAdminAdmins([])
      }
      setNotice({
        type: 'success',
        text: 'Account deleted. Session ended and database entry scrubbed.',
      })
    })
  }

  const refreshAdminTables = async (token = sessions.admin?.token) => {
    if (!token) return
    const [customers, admins] = await Promise.all([
      apiRequest('/api/admin/customers', { token }),
      apiRequest('/api/admin/admins', { token }),
    ])
    setAdminCustomers(customers)
    setAdminAdmins(admins)
  }

  const deleteCustomerAsAdmin = async (customerId) => {
    const token = sessions.admin?.token
    await withNotice(async () => {
      if (!token) throw new Error('Admin login required.')
      await apiRequest(`/api/admin/customers/${customerId}`, { method: 'DELETE', token })
      await refreshAdminTables(token)
      setNotice({ type: 'success', text: `Customer #${customerId} deleted.` })
    })
  }

  const deleteAdminFromRow = async (adminUserId) => {
    const currentAdminUserId = sessions.admin?.profile?.user?.id
    if (adminUserId !== currentAdminUserId) {
      setNotice({ type: 'error', text: 'Admins can only delete their own admin account.' })
      return
    }
    setActivePortal('admin')
    await deleteSelf()
  }

  const handleSort = (column) => {
    if (sortColumn === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
    } else {
      setSortColumn(column)
      setSortOrder('asc')
    }
  }

  const getSortedAndFilteredCustomers = () => {
    let filtered = adminCustomers
    if (showPremiumOnly) {
      filtered = filtered.filter((c) => Number(c.account.balance) > 10000)
    }
    return filtered.sort((a, b) => {
      let aVal, bVal
      switch (sortColumn) {
        case 'id':
          aVal = a.id
          bVal = b.id
          break
        case 'name':
          aVal = a.name.toLowerCase()
          bVal = b.name.toLowerCase()
          break
        case 'type':
          aVal = a.account.account_type
          bVal = b.account.account_type
          break
        case 'balance':
          aVal = Number(a.account.balance)
          bVal = Number(b.account.balance)
          break
        default:
          return 0
      }
      if (aVal < bVal) return sortOrder === 'asc' ? -1 : 1
      if (aVal > bVal) return sortOrder === 'asc' ? 1 : -1
      return 0
    })
  }

  const getSortIndicator = (column) => {
    if (sortColumn !== column) return ''
    return sortOrder === 'asc' ? ' ▲' : ' ▼'
  }

  const splash = useMemo(() => {
    if (!session?.profile) return null
    const { user, entity_id: entityId, account } = session.profile
    if (account) {
      return `${roleLabel.splash}: ${user.name} (#${user.id}) | Account #${account.id} | Entity #${entityId}`
    }
    return `${roleLabel.splash}: ${user.name} (#${user.id}) | Admin Entity #${entityId}`
  }, [session, roleLabel.splash])

  return (
    <main className="shell">
      <header className="hero">
        <p className="kicker">Big</p>
        <h1>Banking Identity Console</h1>
        <p>Two isolated environments with encrypted passwords: Customer and Admin.</p>
      </header>

      <section className="panel connection-panel">
        <div className="tabs">
          <button
            type="button"
            className={activePortal === 'customer' ? 'tab active' : 'tab'}
            onClick={() => setActivePortal('customer')}
          >
            Customer Portal
          </button>
          <button
            type="button"
            className={activePortal === 'admin' ? 'tab active' : 'tab'}
            onClick={() => setActivePortal('admin')}
          >
            Admin Portal
          </button>
        </div>
      </section>

      <section className="panel auth-panel">
        <div>
          {!session ? (
            <>
              <h2>{roleLabel.title} {isRegisterMode ? 'Register' : 'Login'}</h2>
              <p className="muted">
                {isRegisterMode
                  ? 'Create your credentials to access this portal.'
                  : 'Sign in with your existing credentials.'}
              </p>
              <label>
                Name
                <input
                  value={forms[activePortal].name}
                  onChange={(event) => updateForm(activePortal, 'name', event.target.value)}
                />
              </label>
              <label>
                Password
                <input
                  type="password"
                  value={forms[activePortal].password}
                  onChange={(event) => updateForm(activePortal, 'password', event.target.value)}
                />
              </label>
              {isRegisterMode ? (
                <label>
                  Register Token
                  <input
                    type="password"
                    value={forms[activePortal].register_token}
                    onChange={(event) => updateForm(activePortal, 'register_token', event.target.value)}
                  />
                </label>
              ) : null}
              {isRegisterMode && activePortal === 'customer' ? (
                <>
                  <label>
                    Account Type
                    <select
                      value={forms[activePortal].account_type}
                      onChange={(event) => updateForm(activePortal, 'account_type', event.target.value)}
                    >
                      <option value="savings">Savings</option>
                      <option value="checking">Checking</option>
                    </select>
                  </label>
                  <label>
                    Initial Balance
                    <input
                      type="number"
                      step="0.01"
                      value={forms[activePortal].balance}
                      onChange={(event) => updateForm(activePortal, 'balance', event.target.value)}
                    />
                  </label>
                </>
              ) : null}
              <div className="actions">
                <button
                  type="button"
                  onClick={() => (isRegisterMode ? register(activePortal) : login(activePortal))}
                  disabled={loading}
                >
                  {isRegisterMode ? 'Register' : 'Login'}
                </button>
              </div>
              <p className="auth-footer">
                {isRegisterMode ? 'Already have an account?' : "Don't have an account?"}{' '}
                <button type="button" className="auth-switch" onClick={toggleAuthView} disabled={loading}>
                  {isRegisterMode ? 'Login' : 'Register'}
                </button>
              </p>
            </>
          ) : (
            <>
              <h2>{roleLabel.title} Session</h2>
              <p className="muted">You are signed in. Use these actions to refresh or logout.</p>
              <div className="actions">
                <button type="button" className="ghost" onClick={() => refreshMe(activePortal)} disabled={loading}>
                  Refresh Profile
                </button>
                <button type="button" className="ghost" onClick={() => logout(activePortal)} disabled={loading}>
                  Logout
                </button>
              </div>
            </>
          )}
        </div>

        <div>
          {notice.text ? <p className={`notice ${notice.type || 'neutral'}`}>{notice.text}</p> : null}
          {session?.profile ? (
            <>
              <p className="splash">{splash}</p>
              {activePortal === 'customer' && session.profile.account ? (
                <div className="account-card">
                  <h3>My Account</h3>
                  <p><strong>Balance:</strong> ${Number(session.profile.account.balance).toLocaleString()}</p>
                  <p><strong>Type:</strong> {session.profile.account.account_type}</p>
                </div>
              ) : (
                <div className="account-card">
                  <h3>Admin Profile</h3>
                  <p><strong>Access:</strong> Administrative controls only.</p>
                </div>
              )}

              <label>
                New Name
                <input
                  value={nameUpdate[activePortal]}
                  onChange={(event) =>
                    setNameUpdate((prev) => ({ ...prev, [activePortal]: event.target.value }))
                  }
                />
              </label>
              <button type="button" className="inline-action" onClick={submitNameUpdate} disabled={loading}>
                Save Name
              </button>

              <label>
                New Password
                <input
                  type="password"
                  value={passwordUpdate[activePortal]}
                  onChange={(event) =>
                    setPasswordUpdate((prev) => ({ ...prev, [activePortal]: event.target.value }))
                  }
                />
              </label>
              <button type="button" className="inline-action" onClick={submitPasswordUpdate} disabled={loading}>
                Save Password
              </button>

              {activePortal === 'customer' ? (
                <>
                  <label>
                    Balance Adjustment Amount
                    <input
                      type="number"
                      step="0.01"
                      value={balanceDelta[activePortal]}
                      onChange={(event) =>
                        setBalanceDelta((prev) => ({ ...prev, [activePortal]: event.target.value }))
                      }
                    />
                  </label>
                  <div className="actions">
                    <button type="button" className="green" onClick={() => adjustBalance(1)} disabled={loading}>
                      Add Funds
                    </button>
                    <button type="button" className="orange" onClick={() => adjustBalance(-1)} disabled={loading}>
                      Subtract Funds
                    </button>
                  </div>
                </>
              ) : null}

              <button type="button" className="danger" onClick={deleteSelf} disabled={loading}>
                Delete My Account
              </button>
            </>
          ) : (
            <p className="muted">No active {activePortal} session.</p>
          )}
        </div>
      </section>

      {activePortal === 'admin' && sessions.admin?.profile ? (
        <section className="panel tables-panel">
          <div>
            <h3>Customer Accounts</h3>
            <div className="actions">
              <button type="button" className="ghost" onClick={() => refreshAdminTables()} disabled={loading}>
                Refresh Tables
              </button>
              <button
                type="button"
                className={showPremiumOnly ? 'green' : 'ghost'}
                onClick={() => setShowPremiumOnly(!showPremiumOnly)}
                disabled={loading}
              >
                {showPremiumOnly ? 'Show All Customers' : 'Show Premium Only'}
              </button>
            </div>
            <table>
              <thead>
                <tr>
                  <th onClick={() => handleSort('id')} style={{ cursor: 'pointer' }}>ID{getSortIndicator('id')}</th>
                  <th onClick={() => handleSort('name')} style={{ cursor: 'pointer' }}>Name{getSortIndicator('name')}</th>
                  <th onClick={() => handleSort('type')} style={{ cursor: 'pointer' }}>Type{getSortIndicator('type')}</th>
                  <th onClick={() => handleSort('balance')} style={{ cursor: 'pointer' }}>Balance{getSortIndicator('balance')}</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {getSortedAndFilteredCustomers().map((customer) => {
                  const isPremium = Number(customer.account.balance) > 10000
                  return (
                    <tr key={customer.id} style={{ backgroundColor: isPremium ? '#fef3e5' : 'inherit' }}>
                      <td>{customer.id}</td>
                      <td>{customer.name}</td>
                      <td>{customer.account.account_type}</td>
                      <td>${Number(customer.account.balance).toLocaleString()}</td>
                      <td>
                        <button
                          type="button"
                          className="danger"
                          onClick={() => deleteCustomerAsAdmin(customer.id)}
                          disabled={loading}
                        >
                          Delete Customer
                        </button>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>

          <div>
            <h3>Admin Accounts</h3>
            <table>
              <thead>
                <tr>
                  <th>Admin ID</th>
                  <th>User ID</th>
                  <th>Name</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {adminAdmins.map((adminRow) => {
                  const isSelf = adminRow.user_id === sessions.admin.profile.user.id
                  return (
                    <tr key={adminRow.id}>
                      <td>{adminRow.id}</td>
                      <td>{adminRow.user_id}</td>
                      <td>{adminRow.name}</td>
                      <td>
                        <button
                          type="button"
                          className={isSelf ? 'danger' : 'ghost'}
                          onClick={() => deleteAdminFromRow(adminRow.user_id)}
                          disabled={loading || !isSelf}
                        >
                          {isSelf ? 'Delete My Admin Account' : 'Protected'}
                        </button>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </section>
      ) : null}
    </main>
  )
}

export default App
