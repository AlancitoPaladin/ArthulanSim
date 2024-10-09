package com.itsm.aartrad.models

import com.itsm.aartrad.R
import com.itsm.aartrad.navigation.NavScreen

sealed class ItemsBottomNav(
    val icon: Int,
    val title: String,
    val route: String
) {
    object ItemBottomNav1 : ItemsBottomNav(
        icon = R.drawable.wallet,
        title = "Cartera",
        NavScreen.WalletScreen.name
    )
    object ItemBottomNav2 : ItemsBottomNav(
        icon = R.drawable.loginlogo,
        title = "Mercado",
        NavScreen.CryptoScreen.name
    )
    object ItemBottomNav3 : ItemsBottomNav(
        icon = R.drawable.history,
        title = "Historial",
        NavScreen.HistoryScreen.name
    )
}