package com.itsm.aartrad.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.itsm.aartrad.screens.CryptoScreen
import com.itsm.aartrad.screens.HistoryScreen
import com.itsm.aartrad.screens.WalletScreen

@Composable
fun MainNavigation(
    navController: NavHostController
) {
    NavHost(
        navController = navController,
        startDestination = NavScreen.CryptoScreen.name
    ) {
        composable(NavScreen.CryptoScreen.name) {
            CryptoScreen(navController)
        }
        composable(NavScreen.HistoryScreen.name) {
            HistoryScreen(navController)
        }
        composable(NavScreen.WalletScreen.name) {
            WalletScreen(navController)
        }
    }
}
