import React from "react";
import ReviewedItems from "./components/ReviewedItems";
import User from "./components/Users";
import { GetRecommender1, GetRecommender2 } from "./components/Recommendations";
import Recommendations from "./components/Recommendations";

window.$user = 'AUGLMQUVDU21Z'
window.$recommender1 = 'vgg'
window.$recommender2 = 'random'

export default function App() {



  return (

    <main class="main" id="top">
      <nav class="navbar navbar-expand-lg navbar-light fixed-top py-3 d-block" data-navbar-on-scroll="data-navbar-on-scroll">
        <div class="container"><a class="navbar-brand d-inline-flex" href="#"><span class="text-1000 fs-0 fw-bold ms-2">Usuarios:</span></a><button class="navbar-toggler collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation"><span class="navbar-toggler-icon"></span></button>
          <div class="collapse navbar-collapse border-top border-lg-0 mt-4 mt-lg-0" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <User />
            </ul>
          </div>
        </div>
      </nav>
      <section class="py-11 bg-light-gradient border-bottom border-white border-5">
        <div class="bg-holder overlay overlay-light" style={{ backgroundImage: "url(assets/img/gallery/header-bg.png)", backgroundSize: "cover" }}></div>

        <div class="container">
          <div class="row flex-center">
            <div class="col-12 mb-10">
              <div class="d-flex align-items-center flex-column">

                <h1 class="fs-4 fs-lg-8 fs-md-6 fw-bold">Aprendizaje profundo y la moda</h1>
                <h1 class="fw-normal"> Patricia Matos</h1>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section>
        <div class="container">
          <div class="col-lg-7 mx-auto text-center mb-6">
            <h4 class="fs-3 fs-lg-4 lh-sm mb-3">Items valorados por el usuario</h4>
          </div>


          <ReviewedItems />
          <div class="row h-100 g-2 py-1 text-center" id="valorados">

          </div>
        </div>
      </section>

      <section class="py-0">
        <div class="container">
          <div class="col-lg-7 mx-auto text-center mb-6">
            <h2 class="fs-3 fs-lg-5 lh-sm mb-3">Recomendaciones </h2>
          </div>
          <div class="row h-100">
            <div class="col-lg-5 mx-auto text-center mb-6">
              <div className="dd-wrapper">
                <div className="dd-header">
                  <div className="dd-header-title fs-lg-1">Recomendador 1</div>
                </div>
                <select className="dd-list" id="recommender1" onChange={GetRecommender1}>

                  <option className="dd-list-item" value='vgg' selected>VGG-16</option>
                  <option className="dd-list-item" value='incpt'>Inception-V3</option>
                  <option className="dd-list-item" value='resnet'>Resnet 50</option>
                  <option className="dd-list-item" value='cf'>Collaborative</option>
                  <option className="dd-list-item" value='random'>Random Baseline</option>
                  <option className="dd-list-item" value='popularity'>Popularity Baseline</option>

                </select>
              </div>
            </div>
            <div class="col-lg-2 mx-auto text-center mb-6">
              <h5 class="fs-3 fs-lg-3 mb-3">vs.</h5>
            </div>
            <div class="col-lg-5 mx-auto text-center mb-6">
              <div className="dd-wrapper">
                <div className="dd-header">
                  <div className="dd-header-title fs-lg-1">Recomendador 2</div>
                </div>
                <select className="dd-list" id="recommender2" onChange={GetRecommender2}>

                  <option className="dd-list-item" value='vgg'>VGG-16</option>
                  <option className="dd-list-item" value='incpt'>Inception-V3</option>
                  <option className="dd-list-item" value='resnet'>Resnet 50</option>
                  <option className="dd-list-item" value='cf'>Collaborative</option>
                  <option className="dd-list-item" value='random' selected>Random Baseline</option>
                  <option className="dd-list-item" value='popularity'>Popularity Baseline</option>

                </select>
              </div>
            </div>
          </div>


          <div class="container">
            <div class="row h-100">
              <div class="col-lg-7 mx-auto text-center mb-6">
                <h6 class="fs-3 fs-lg-3 lh-sm mb-3" id="r1">Recomendaciones via {window.$recommender1} </h6>
              </div>
              {GetRecommender1()}
              <div class="col-12">
                <div class="carousel slide" id="carouselNewArrivals" data-bs-ride="carousel">
                  <div class="carousel-inner">
                    <div class="carousel-item active" data-bs-interval="10000">
                      <div class="row h-100 align-items-center g-2" id="recomendaciones">
                      </div>
                    </div>

                    <div class="carousel-item " data-bs-interval="5000">
                      <div class="row h-100 align-items-center g-2" id="recomendaciones2">

                      </div>
                    </div>
                    <div class="carousel-item" data-bs-interval="5000">
                      <div class="row h-100 align-items-center g-2" id="recomendaciones3">

                      </div>
                    </div>

                    <div class="row"><button class="carousel-control-prev" type="button" data-bs-target="#carouselNewArrivals" data-bs-slide="prev"><span class="carousel-control-prev-icon" aria-hidden="true"></span><span class="visually-hidden">Previous</span></button><button class="carousel-control-next" type="button" data-bs-target="#carouselNewArrivals" data-bs-slide="next"><span class="carousel-control-next-icon" aria-hidden="true"></span><span class="visually-hidden">Next </span></button></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="row h-100">
            <div class="col-lg-7 mx-auto text-center mb-6">
              <h5 class="fs-3 fs-lg-5 lh-sm mb-3"></h5>
            </div>
          </div>

          <div class="container">
            <div class="row h-100">
              <div class="col-lg-7 mx-auto text-center mb-6">
                <h5 class="fs-3 fs-lg-3 lh-sm mb-3" id="r2">Recomendaciones via {window.$recommender2}</h5>
              </div>
              {GetRecommender2()}
              <div class="col-12">
                <div class="carousel slide" id="carouselNewArrivals2" data-bs-ride="carousel">
                  <div class="carousel-inner">
                    <div class="carousel-item active" data-bs-interval="10000">
                      <div class="row h-100 align-items-center g-2" id="recomendaciones4">
                      </div>
                    </div>

                    <div class="carousel-item " data-bs-interval="5000">
                      <div class="row h-100 align-items-center g-2" id="recomendaciones5">

                      </div>
                    </div>
                    <div class="carousel-item" data-bs-interval="5000">
                      <div class="row h-100 align-items-center g-2" id="recomendaciones6">

                      </div>
                    </div>

                    <div class="row"><button class="carousel-control-prev" type="button" data-bs-target="#carouselNewArrivals2" data-bs-slide="prev"><span class="carousel-control-prev-icon" aria-hidden="true"></span><span class="visually-hidden">Previous</span></button><button class="carousel-control-next" type="button" data-bs-target="#carouselNewArrivals2" data-bs-slide="next"><span class="carousel-control-next-icon" aria-hidden="true"></span><span class="visually-hidden">Next </span></button></div>
                  </div>
                </div>
              </div>
            </div>
          </div>


        </div>
      </section>

    </main>
  );
}