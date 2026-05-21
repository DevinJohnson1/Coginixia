import React from 'react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

beforeEach(() => {
  vi.restoreAllMocks()
})

describe('App', () => {
  it('renders customer login by default', () => {
    render(<App />)

    expect(screen.getByRole('heading', { name: /banking identity console/i })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: /customer portal login/i })).toBeInTheDocument()
  })

  it('switches to admin portal login', async () => {
    const user = userEvent.setup()
    render(<App />)

    await user.click(screen.getByRole('button', { name: /admin portal/i }))

    expect(screen.getByRole('heading', { name: /admin portal login/i })).toBeInTheDocument()
  })

  it('shows validation notice when login fields are empty', async () => {
    const user = userEvent.setup()
    const fetchSpy = vi.spyOn(globalThis, 'fetch')
    render(<App />)

    await user.click(screen.getByRole('button', { name: /^login$/i }))

    expect(screen.getByText(/name and password are required/i)).toBeInTheDocument()
    expect(fetchSpy).not.toHaveBeenCalled()
  })

  it('logs in customer and stores auth token for follow-up requests', async () => {
    const user = userEvent.setup()
    const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => ({
        token: 'token-123',
        profile: {
          user: { id: 1, name: 'Ada', role: 'customer' },
          entity_id: 1,
          account: { id: 10, account_type: 'savings', balance: 1250 },
        },
      }),
    })

    render(<App />)

    await user.type(screen.getByLabelText(/name/i), 'Ada')
    await user.type(screen.getByLabelText(/password/i), 'strong-pass')
    await user.click(screen.getByRole('button', { name: /^login$/i }))

    expect(fetchSpy).toHaveBeenCalledWith(
      expect.stringContaining('/api/auth/login/customer'),
      expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({ 'Content-Type': 'application/json' }),
      }),
    )
    expect(await screen.findByText(/welcome back, ada/i)).toBeInTheDocument()
  })

  it('blocks registration when register token is missing', async () => {
    const user = userEvent.setup()
    const fetchSpy = vi.spyOn(globalThis, 'fetch')
    render(<App />)

    await user.click(screen.getByRole('button', { name: /register/i }))
    await user.type(screen.getByLabelText(/name/i), 'Ada')
    await user.type(screen.getByLabelText(/password/i), 'strong-pass')
    await user.click(screen.getByRole('button', { name: /^register$/i }))

    expect(screen.getByText(/name, password, and register token are required/i)).toBeInTheDocument()
    expect(fetchSpy).not.toHaveBeenCalled()
  })
})




