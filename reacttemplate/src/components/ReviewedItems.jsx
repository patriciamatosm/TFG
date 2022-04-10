import React, { useEffect, useState } from "react";

const ReviewedItemsContext = React.createContext({
    reviewedItems: [], fetchReviewedItems: () => { }
});

export async function GetReviewedItems() {
    const response = await fetch("http://localhost:8000/reviewedItems/" + window.$user)
    const reviewedItems = await response.json()
    console.log(reviewedItems)
    const divi = document.querySelector('#valorados')
    divi.replaceChildren()
    return (

        Object.entries(reviewedItems).map(
            ([key, value]) => {
                const div1 = document.createElement("div");
                div1.setAttribute("class", "col-md-2 text-center")

                const div2 = document.createElement("div");
                div2.setAttribute("class", "card card-span h-100 text-white")

                const img = document.createElement("img");
                img.src = value;
                img.setAttribute("class", "card-img h-100")

                const div3 = document.createElement("div");
                div3.setAttribute("class", "card-img-overlay bg-dark-gradient")

                const div4 = document.createElement("div");
                div4.setAttribute("class", "d-flex align-items-end justify-content-center h-100")

                const a = document.createElement("a");
                a.setAttribute("class", "btn btn-lg text-light fs-1")
                a.setAttribute("role", "button")
                a.innerHTML = key;

                div4.appendChild(a)
                div3.appendChild(div4)


                div2.appendChild(img)
                div2.appendChild(div3)
                div1.appendChild(div2)

                divi.appendChild(div1)
            }
        )
    );

}

export default function ReviewedItems() {
    const [reviewedItems, setReviewedItems] = useState([])
    const fetchReviewedItems = async () => {
        const response = await fetch("http://localhost:8000/reviewedItems/" + window.$user)
        const reviewedItems = await response.json()
        setReviewedItems(reviewedItems)
        console.log(reviewedItems)
    }
    const divi = document.querySelector('#valorados')

    useEffect(() => {
        fetchReviewedItems()
    }, [])
    return (
        <ReviewedItemsContext.Provider value={{ reviewedItems, fetchReviewedItems }}>

            {
                Object.entries(reviewedItems).map(
                    ([key, value]) => {

                        divi.replaceChildren()
                        const div1 = document.createElement("div");
                        div1.setAttribute("class", "col-md-2 text-center")

                        const div2 = document.createElement("div");
                        div2.setAttribute("class", "card card-span h-100 text-white")

                        const img = document.createElement("img");
                        img.src = value;
                        img.setAttribute("class", "card-img h-100")

                        const div3 = document.createElement("div");
                        div3.setAttribute("class", "card-img-overlay bg-dark-gradient")

                        const div4 = document.createElement("div");
                        div4.setAttribute("class", "d-flex align-items-end justify-content-center h-100")

                        const a = document.createElement("a");
                        a.setAttribute("class", "btn btn-lg text-light fs-1")
                        a.setAttribute("role", "button")
                        a.innerHTML = key;

                        div4.appendChild(a)
                        div3.appendChild(div4)
                        div2.appendChild(img)
                        div2.appendChild(div3)
                        div1.appendChild(div2)

                        divi.appendChild(div1)

                    }
                )
            }
        </ReviewedItemsContext.Provider>
    )
}