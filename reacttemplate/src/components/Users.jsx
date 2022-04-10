import React, { useEffect, useState } from "react";
import { GetReviewedItems } from "./ReviewedItems";


export function GetSelectedUser(event) {

  console.log('aqui')
  if (window.$user != null) {
    if (document.querySelector("#usersSelect")) {
      window.$user = document.getElementById("usersSelect").value;

    }
  }


  const divi = document.querySelector('#recomendaciones')
  divi.replaceChildren()
  const divi2 = document.querySelector('#recomendaciones2')
  divi2.replaceChildren()
  const divi3 = document.querySelector('#recomendaciones3')
  divi3.replaceChildren()

  const div = document.querySelector('#recomendaciones4')
  div.replaceChildren()
  const div2 = document.querySelector('#recomendaciones5')
  div2.replaceChildren()
  const div3 = document.querySelector('#recomendaciones6')
  div3.replaceChildren()


  document.getElementById("r1").innerHTML = ""
  document.getElementById("r2").innerHTML = ""

  GetReviewedItems()
  console.log(window.$user) // Ejecutar recomendacion when change
}



const UserContext = React.createContext({
  user: [], fetchUsers: () => { }
})

export default function User() {
  const [users, setUsers] = useState([])


  const fetchUsers = async () => {
    const response = await fetch("http://localhost:8000/users")
    const users = await response.json()
    console.log(users)
    setUsers(users)
    console.log(users)
  }
  useEffect(() => {
    fetchUsers()

  }, [])
  return (
    <UserContext.Provider value={{ users, fetchUsers }}>
      <div className="dd-wrapper">
        <div className="dd-header">
          <div className="dd-header-title"></div>
        </div>
        <select className="dd-list" id="usersSelect" onChange={GetSelectedUser}>

          {
            users.map(user => (
              <option className="dd-list-item" key={user}>{user}</option>
            )
            )

          }

        </select>
      </div>
    </UserContext.Provider>
  )
}

