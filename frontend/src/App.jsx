import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <section id = "login">
        <h1>Login Info</h1>

        <div id = "login-form">
          <input type = "text" placeholder = "username" id = "username"></input>
          <input type = "password" placeholder = "password" id = "password"></input>
          <p></p>
          <a href="">forget password?</a>
          <p></p>
          <button type = "submit" id = "sign-in-btn">sign in</button>
          <button type="submit" id = "sing-up-btn">sign up</button>
          <p></p>
          <a href="">contact us to get more information</a>
        </div>
      </section>
    </>
  )
}

export default App
