<template>
  <div id="wrappr">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>San Andreas Games</strong></router-link>
        <a class="navbar-burger" aria-label="false" data-target="navbar-menu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>
      <div class="navbar-menu" id="navbar-menu">
        <div class="navbar-end">
          <router-link to="/disk" class="navbar-item">Disk</router-link>
          <router-link to="/digital" class="navbar-item">Digital</router-link>
          <div class="navbar-item">
            <div class="buttons">
              <router-link to="/log-in" class="button is-light">Log in</router-link>
              <router-link to="/cart" class="button is-success">
                <span>Cart</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>
    <section class="section">
      <router-view/>
    </section>
    <footer class="has-text-centered">
      <p>Created by Adel</p>
    </footer>
  </div>
</template>

<style lang="scss">
@import "../node_modules/bulma";
</style>
