<template>
    <v-app id="app">
        <Header @updateYear="updateYear()" />

        <v-main class="main-content">
            <router-view />
        </v-main>

        <Footer />
    </v-app>
</template>

<script>

import Header from './components/Header';
import Footer from './components/Footer';

import { DARK_MODE, DEFAULT_DARK_MODE } from './data/vuex.js'

export default {
    name: 'App',
    components: {
        Header,
        Footer
    },
    data: () => ({
        deleteClicked: false,
        searchInput: '',
        extension: ''
    }),
    mounted() {
        // Load dark mode directly from localStorage for faster response time
        // Note: localStorage saves as a string
        let darkMode = localStorage.getItem(DARK_MODE);
        this.$vuetify.theme.dark = darkMode === null ? DEFAULT_DARK_MODE : darkMode === 'true';
    }
}
</script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap');
</style>    

<style lang="scss">
  @import '@/styles/_globals.scss';
</style>

