# 問題

![001.png](問題)

# 解法

時間内に解けたことは解けたのだけどadmin、adminで入った場合にBalanceがめちゃめちゃ増えてて(たぶん他の人が解いた)あっさり解けてしまった。
チーム内でこれ違うよね、との議論になって終わった後にwriteupみてたらやっぱり違った。

チームメンバーが```robots.txt```を見つけてくれてその中には
```text
Disallow: /shop-1.0.0.war
```
と書かれている。
shop-1.0.0.warはサーブレットのメイン。
JDCだとなぜかShopController.javaがデコンパイルできないファイルがあったのでLuytenを使った。

```java
package ru.volgactf.shop.controllers;

import org.springframework.stereotype.*;
import org.springframework.beans.factory.annotation.*;
import ru.volgactf.shop.dao.*;
import org.springframework.web.bind.*;
import org.springframework.ui.*;
import javax.servlet.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.*;
import ru.volgactf.shop.models.*;
import java.util.*;

@Controller
public class ShopController
{
    @Autowired
    private UserDao userDao;
    @Autowired
    private ProductDao productDao;
    
    @InitBinder
    public void initBinder(final WebDataBinder binder) {
        binder.setDisallowedFields(new String[] { "balance" });
    }
    
    @ModelAttribute("user")
    public User getUser(final HttpServletRequest request) {
        return (User)((request.getAttribute("user") != null) ? request.getAttribute("user") : new User());
    }
    
    @RequestMapping({ "", "/", "/index" })
    public String index(@ModelAttribute("message") final String message, @ModelAttribute("user") final User user, final Model templateModel) {
        templateModel.addAttribute("products", (Object)this.productDao.geProducts());
        return "shop";
    }
    
    @RequestMapping({ "/login" })
    public String login(@ModelAttribute("message") final String message) {
        return "login";
    }
    
    @RequestMapping({ "/registration" })
    public String registration(@ModelAttribute("message") final String message) {
        return "registration";
    }
    
    @RequestMapping({ "/logout" })
    public String registration(final HttpServletRequest request) {
        final HttpSession session = request.getSession();
        session.setAttribute("user_id", (Object)null);
        return "redirect:index";
    }
    
    @RequestMapping({ "/loginProcess" })
    public String login(@RequestParam final String name, @RequestParam final String pass, final Model templateModel, final RedirectAttributes redir, final HttpServletRequest request) {
        final HttpSession session = request.getSession();
        final User user = this.userDao.login(name, pass);
        if (user != null) {
            session.setAttribute("user_id", (Object)user.getId());
            redir.addFlashAttribute("message", (Object)"Successful login");
            return "redirect:index";
        }
        redir.addFlashAttribute("message", (Object)"Invalid username or password");
        return "redirect:login";
    }
    
    @RequestMapping({ "/registrationProcess" })
    public String registration(@RequestParam final String name, @RequestParam final String pass, final Model templateModel, final RedirectAttributes redir, final HttpServletRequest request) {
        final HttpSession session = request.getSession();
        if (this.userDao.findByName(name) == null) {
            final User user = this.userDao.register(name, pass);
            session.setAttribute("user_id", (Object)user.getId());
            redir.addFlashAttribute("message", (Object)"Successful registration");
            return "redirect:index";
        }
        redir.addFlashAttribute("message", (Object)"User already exists");
        return "redirect:registration";
    }
    
    @RequestMapping({ "/profile" })
    public String profile(@ModelAttribute("user") final User user, final Model templateModel, final HttpServletRequest request) {
        final HttpSession session = request.getSession();
        if (session.getAttribute("user_id") == null) {
            return "redirect:index";
        }
        final List<Product> cart = new ArrayList<Product>();
        user.getCartItems().forEach(p -> cart.add(this.productDao.geProduct(p.getId())));
        templateModel.addAttribute("cart", (Object)cart);
        return "profile";
    }
    
    @RequestMapping({ "/buy" })
    public String buy(@RequestParam final Integer productId, @ModelAttribute("user") final User user, final RedirectAttributes redir, final HttpServletRequest request) {
        final HttpSession session = request.getSession();
        if (session.getAttribute("user_id") == null) {
            return "redirect:index";
        }
        final Product product = this.productDao.geProduct(productId);
        if (product != null) {
            if (product.getPrice() <= user.getBalance()) {
                user.setBalance(Integer.valueOf(user.getBalance() - product.getPrice()));
                user.getCartItems().add(product);
                this.userDao.update(user);
                redir.addFlashAttribute("message", (Object)"Successful purchase");
                return "redirect:profile";
            }
            redir.addFlashAttribute("message", (Object)"Not enough money");
        }
        else {
            redir.addFlashAttribute("message", (Object)"Product not found");
        }
        return "redirect:index";
    }
}
```

単純なJSP。
JSPだとGETとPOSTが同じように扱われるのを知っていたので
shop.q.2019.volgactf.ru/buy?productId=1
にアクセスして購入できたりするのは確認。
ここでどん詰まった後にadminで入れて解けたのだが、正解は違うっぽい。
正解は
http:\\shop.q.2019.volgactf.ru/buy?productId=4&Balance=10000
でBalanceを書き換えて購入するとのことだった。

ただ、デコンパイルしたファイルを見てもBalanceは書き換えられないように見える。framework使うと勝手にBalanceも外からいじれるようになるとかだろうか。後で自分の手元で試してみたい．．．

# 参考

- [VolgaCTF - Shop [ WEB ] [DeadLock Team ] [ 2019 ] [ Writeup ] - YouTube](https://www.youtube.com/watch?v=Xx8JoCOnUM0)
