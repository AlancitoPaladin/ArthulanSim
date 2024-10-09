package com.itsm.aartrad.components

import androidx.compose.material3.BottomAppBar
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.navigation.NavHostController
import com.itsm.aartrad.models.ItemsBottomNav.ItemBottomNav1
import com.itsm.aartrad.models.ItemsBottomNav.ItemBottomNav2
import com.itsm.aartrad.models.ItemsBottomNav.ItemBottomNav3
import com.itsm.aartrad.navigation.currentRoute

@Composable
fun LowNavigation(navController: NavHostController) {
    val menuItems = listOf(
        ItemBottomNav1,
        ItemBottomNav2,
        ItemBottomNav3
    )

    BottomAppBar(
        containerColor = Color.Black
    ) {
        NavigationBar(
            containerColor = Color.Black
        ) {
            menuItems.forEach { item ->
                val selected = currentRoute(navController) == item.route
                NavigationBarItem(
                    selected = selected,
                    onClick = { navController.navigate(item.route) },
                    icon = {
                        Icon(
                            painter = painterResource(id = item.icon),
                            contentDescription = item.title,
                            tint = Color.White
                        )
                    },
                    label = {
                        Text(text = item.title, color = Color.White)
                    },
                    colors = NavigationBarItemDefaults.colors(
                        selectedIconColor = Color.White,
                        unselectedIconColor = Color.White,
                        selectedTextColor = Color.White,
                        unselectedTextColor = Color.White,
                        indicatorColor = Color(0xFF0A9597)
                    )
                )
            }
        }
    }
}
