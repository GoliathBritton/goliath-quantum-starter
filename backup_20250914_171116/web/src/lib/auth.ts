import { NextAuthOptions } from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'
import { JWT } from 'next-auth/jwt'

interface User {
  id: string
  email: string
  first_name: string
  last_name: string
  role: string
  partner_id?: string
  access_token: string
}

interface LoginResponse {
  access_token: string
  token_type: string
  expires_in: number
  user_id: string
  email: string
  role: string
  partner_id?: string
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: 'credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' }
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null
        }

        try {
          const response = await fetch(`${API_URL}/api/auth/login`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              email: credentials.email,
              password: credentials.password,
            }),
          })

          if (!response.ok) {
            return null
          }

          const loginData: LoginResponse = await response.json()

          // Fetch user details
          const userResponse = await fetch(`${API_URL}/api/auth/me`, {
            headers: {
              'Authorization': `Bearer ${loginData.access_token}`,
            },
          })

          if (!userResponse.ok) {
            return null
          }

          const userData = await userResponse.json()

          return {
            id: loginData.user_id,
            email: loginData.email,
            first_name: userData.first_name,
            last_name: userData.last_name,
            role: loginData.role,
            partner_id: loginData.partner_id,
            access_token: loginData.access_token,
          } as User
        } catch (error) {
          console.error('Authentication error:', error)
          return null
        }
      },
    }),
  ],
  session: {
    strategy: 'jwt',
    maxAge: 30 * 60, // 30 minutes
  },
  callbacks: {
    async jwt({ token, user }: { token: JWT; user?: User }) {
      if (user) {
        token.id = user.id
        token.email = user.email
        token.first_name = user.first_name
        token.last_name = user.last_name
        token.role = user.role
        token.partner_id = user.partner_id
        token.access_token = user.access_token
      }
      return token
    },
    async session({ session, token }) {
      if (token) {
        session.user = {
          id: token.id as string,
          email: token.email as string,
          first_name: token.first_name as string,
          last_name: token.last_name as string,
          role: token.role as string,
          partner_id: token.partner_id as string | undefined,
        }
        session.access_token = token.access_token as string
      }
      return session
    },
  },
  pages: {
    signIn: '/sign-in',
    error: '/sign-in',
  },
  secret: process.env.NEXTAUTH_SECRET,
}

// Extend the built-in session types
declare module 'next-auth' {
  interface Session {
    user: {
      id: string
      email: string
      first_name: string
      last_name: string
      role: string
      partner_id?: string
    }
    access_token: string
  }
}

declare module 'next-auth/jwt' {
  interface JWT {
    id: string
    email: string
    first_name: string
    last_name: string
    role: string
    partner_id?: string
    access_token: string
  }
}