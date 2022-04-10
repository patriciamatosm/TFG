import React, { useEffect, useState } from "react";

export function GetRecommender1(event) {
  
    if (window.$recommender1 != null) {
      if (document.querySelector("#recommender1")) {
        window.$recommender1 = document.getElementById("recommender1").value;
        document.getElementById("r1").innerHTML = "Recomendaciones via " + window.$recommender1
      }
    }
    GetRecommendations1()
  }

  export function GetRecommender2(event) {
  
    if (window.$recommender2 != null) {
      if (document.querySelector("#recommender2")) {
        window.$recommender2 = document.getElementById("recommender2").value;
        document.getElementById("r2").innerHTML = "Recomendaciones via " + window.$recommender2
          
      }
    }
    GetRecommendations2()
  }

const RecommedationsContext = React.createContext({
    todos: [], fetchTodos: () => { }
});

export async function GetRecommendations1() {
    const response = await fetch("http://localhost:8000/recommendation/" + window.$recommender1 + "/" + window.$user)
    const todos = await response.json()
    console.log(todos)
    const divi = document.querySelector('#recomendaciones')
    divi.replaceChildren()
    const divi2 = document.querySelector('#recomendaciones2')
    divi2.replaceChildren()
    const divi3 = document.querySelector('#recomendaciones3')
    divi3.replaceChildren()
    return (


        Object.entries(todos).slice(0, 4).map(
            ([key, value]) => {
                const div1 = document.createElement("div");
                div1.setAttribute("class", "col-sm-6 col-md-3 mb-3 mb-md-0 h-100")

                const div2 = document.createElement("div");
                div2.setAttribute("class", "card card-span h-100 text-white")

                const img = document.createElement("img");
                img.setAttribute("src", value)
                img.setAttribute("class", "card-img h-100")

                const div3 = document.createElement("div");
                div3.setAttribute("class", "card-img-overlay bg-dark-gradient d-flex flex-column-reverse")

                const p = document.createElement("p");
                p.innerHTML = key;
                p.setAttribute("class", "text-400 fs-1")


                const a = document.createElement("a");
                a.setAttribute("class", "stretched-link")

                div3.appendChild(p)
                div2.appendChild(img)
                div2.appendChild(div3)
                div2.appendChild(a)
                div1.appendChild(div2)
                divi.appendChild(div1)
            }
        ),

        Object.entries(todos).slice(4, 8).map(
            ([key, value]) => {
                const div1 = document.createElement("div");
                div1.setAttribute("class", "col-sm-6 col-md-3 mb-3 mb-md-0 h-100")

                const div2 = document.createElement("div");
                div2.setAttribute("class", "card card-span h-100 text-white")

                const img = document.createElement("img");
                img.setAttribute("src", value)
                img.setAttribute("class", "card-img h-100")

                const div3 = document.createElement("div");
                div3.setAttribute("class", "card-img-overlay bg-dark-gradient d-flex flex-column-reverse")

                const p = document.createElement("p");
                p.innerHTML = key;
                p.setAttribute("class", "text-400 fs-1")


                const a = document.createElement("a");
                a.setAttribute("class", "stretched-link")

                div3.appendChild(p)
                div2.appendChild(img)
                div2.appendChild(div3)
                div2.appendChild(a)
                div1.appendChild(div2)
                divi2.appendChild(div1)
            }
        ),

        Object.entries(todos).slice(8, 12).map(
            ([key, value]) => {
                const div1 = document.createElement("div");
                div1.setAttribute("class", "col-sm-6 col-md-3 mb-3 mb-md-0 h-100")

                const div2 = document.createElement("div");
                div2.setAttribute("class", "card card-span h-100 text-white")

                const img = document.createElement("img");
                img.setAttribute("src", value)
                img.setAttribute("class", "card-img h-100")

                const div3 = document.createElement("div");
                div3.setAttribute("class", "card-img-overlay bg-dark-gradient d-flex flex-column-reverse")

                const p = document.createElement("p");
                p.innerHTML = key;
                p.setAttribute("class", "text-400 fs-1")


                const a = document.createElement("a");
                a.setAttribute("class", "stretched-link")

                div3.appendChild(p)
                div2.appendChild(img)
                div2.appendChild(div3)
                div2.appendChild(a)
                div1.appendChild(div2)
                divi3.appendChild(div1)
            }
        )


    )
}

export async function GetRecommendations2() {
    const response = await fetch("http://localhost:8000/recommendation/" + window.$recommender2 + "/" + window.$user)
    const todos = await response.json()
    console.log(todos)
    const divi = document.querySelector('#recomendaciones4')
    divi.replaceChildren()
    const divi2 = document.querySelector('#recomendaciones5')
    divi2.replaceChildren()
    const divi3 = document.querySelector('#recomendaciones6')
    divi3.replaceChildren()
    return (


        Object.entries(todos).slice(0, 4).map(
            ([key, value]) => {
                const div1 = document.createElement("div");
                div1.setAttribute("class", "col-sm-6 col-md-3 mb-3 mb-md-0 h-100")

                const div2 = document.createElement("div");
                div2.setAttribute("class", "card card-span h-100 text-white")

                const img = document.createElement("img");
                img.setAttribute("src", value)
                img.setAttribute("class", "card-img h-100")

                const div3 = document.createElement("div");
                div3.setAttribute("class", "card-img-overlay bg-dark-gradient d-flex flex-column-reverse")

                const p = document.createElement("p");
                p.innerHTML = key;
                p.setAttribute("class", "text-400 fs-1")


                const a = document.createElement("a");
                a.setAttribute("class", "stretched-link")

                div3.appendChild(p)
                div2.appendChild(img)
                div2.appendChild(div3)
                div2.appendChild(a)
                div1.appendChild(div2)
                divi.appendChild(div1)
            }
        ),

        Object.entries(todos).slice(4, 8).map(
            ([key, value]) => {
                const div1 = document.createElement("div");
                div1.setAttribute("class", "col-sm-6 col-md-3 mb-3 mb-md-0 h-100")

                const div2 = document.createElement("div");
                div2.setAttribute("class", "card card-span h-100 text-white")

                const img = document.createElement("img");
                img.setAttribute("src", value)
                img.setAttribute("class", "card-img h-100")

                const div3 = document.createElement("div");
                div3.setAttribute("class", "card-img-overlay bg-dark-gradient d-flex flex-column-reverse")

                const p = document.createElement("p");
                p.innerHTML = key;
                p.setAttribute("class", "text-400 fs-1")


                const a = document.createElement("a");
                a.setAttribute("class", "stretched-link")

                div3.appendChild(p)
                div2.appendChild(img)
                div2.appendChild(div3)
                div2.appendChild(a)
                div1.appendChild(div2)
                divi2.appendChild(div1)
            }
        ),

        Object.entries(todos).slice(8, 12).map(
            ([key, value]) => {
                const div1 = document.createElement("div");
                div1.setAttribute("class", "col-sm-6 col-md-3 mb-3 mb-md-0 h-100")

                const div2 = document.createElement("div");
                div2.setAttribute("class", "card card-span h-100 text-white")

                const img = document.createElement("img");
                img.setAttribute("src", value)
                img.setAttribute("class", "card-img h-100")

                const div3 = document.createElement("div");
                div3.setAttribute("class", "card-img-overlay bg-dark-gradient d-flex flex-column-reverse")

                const p = document.createElement("p");
                p.innerHTML = key;
                p.setAttribute("class", "text-400 fs-1")


                const a = document.createElement("a");
                a.setAttribute("class", "stretched-link")

                div3.appendChild(p)
                div2.appendChild(img)
                div2.appendChild(div3)
                div2.appendChild(a)
                div1.appendChild(div2)
                divi3.appendChild(div1)
            }
        )


    )
}