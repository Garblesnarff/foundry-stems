import { ButtonHTMLAttributes } from 'react'

export function ForgeButton(props: ButtonHTMLAttributes<HTMLButtonElement>) {
  return <button className="forge-button" {...props} />
}
