import time  
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import os
from colorama import Fore
from urllib.parse import urlparse, parse_qs
metadata = {
     "sites" : [
       {
        "name" : "Mastodon-101010.pl",
        "uri_check" : "https://101010.pl/@{account}",
        "e_code" : 200,
        "e_string" : "@101010.pl",
        "m_string" : "The page you are looking for isn&#39;t here.",
        "m_code" : 404,
        "known" : ["szekspir", "xaphanpl"],
        "cat" : "social"
       },
       {
        "name" : "3DNews",
        "uri_check" : "https://forum.3dnews.tech/member.php?username={account}",
        "e_code" : 200,
        "e_string" : "Просмотр профиля:",
        "m_string" : "Пользователь не зарегистрирован",
        "m_code" : 200,
        "known" : ["bob", "red"],
        "cat" : "social"
       },
       {
        "name" : "247sports",
        "uri_check" : "https://247sports.com/User/{account}/",
        "e_code" : 200,
        "e_string" : "<meta property=",
        "m_string" : "<title>247Sports</title>",
        "m_code" : 404,
        "known" : ["bob", "john"],
        "cat" : "hobby"
       },
       {
        "name" : "35photo",
        "uri_check" : "https://35photo.pro/@{account}/",
        "e_code" : 200,
        "e_string" : "<span title=\"Total photos",
        "m_string" : "Catalogs of professional author",
        "m_code" : 302,
        "known" : ["mike007", "derbal"],
        "cat" : "social"
       },
       {
        "name" : "3dtoday",
        "uri_check" : "https://3dtoday.ru/blogs/{account}",
        "e_code" : 200,
        "e_string" : "Блог владельца 3d-принтера",
        "m_string" : "404 Not Found",
        "m_code" : 302,
        "known" : ["sergei", "vlad"],
        "cat" : "hobby"
       },
       {
        "name" : "7cup",
        "uri_check" : "https://www.7cups.com/@{account}",
        "e_code" : 200,
        "e_string" : "Profile - 7 Cups",
        "m_string" : "Oops! The content you're attempting to access could not be found.",
        "m_code" : 404,
        "known" : [ "john", "jbob"],
        "cat" : "social"
       },
       {
        "name" : "7dach",
        "uri_check" : "https://7dach.ru/profile/{account}",
        "e_code" : 200,
        "e_string" : "Информация / Профиль",
        "m_string" : "<title>Ошибка / 7dach.ru",
        "m_code" : 404,
        "known" : ["lana", "svetlana"],
        "cat" : "social"
       },
       {
        "name" : "21buttons",
        "uri_check" : "https://www.21buttons.com/buttoner/{account}",
        "e_code" : 200,
        "e_string" : "profile-info__profile-data__name",
        "m_string" : "This is not the page you're looking for",
        "m_code" : 404,
        "known" : ["patricialmendro", "ginamariahoffmann", "espeworkout"],
        "cat" : "social"
       },
       {
        "name" : "aaha_chat",
        "uri_check" : "https://www.aahachat.org/profile/{account}/",
        "e_code" : 200,
        "e_string" : "https://www.aahachat.org/profile",
        "m_string" : "<title>Page not found",
        "m_code" : 404,
        "known" : ["crazy", "dog"],
        "cat" : "social"
       },
       {
        "name" : "about.me",
        "uri_check" : "https://about.me/{account}",
        "e_code" : 200,
        "e_string" : " | about.me",
        "m_string" : "<title>about.me</title>",
        "m_code" : 404,
        "known" : ["john", "jill"],
        "cat" : "social"
       },
       {
        "name" : "ACF",
        "uri_check" : "https://support.advancedcustomfields.com/forums/users/{account}/",
        "e_code" : 200,
        "e_string" : "<title>ACF Support",
        "m_string" : "Page Not Found",
        "m_code" : 200,
        "known" : ["mike", "greg"],
        "cat" : "coding"
       },
       {
        "name" : "AdmireMe.VIP",
        "uri_check" : "https://admireme.vip/{account}/",
        "e_code" : 200,
        "e_string" : "creator-stat subscriber",
        "m_string" : "<title>Page Not Found |",
        "m_code" : 404,
        "known" : ["justjessicarabbit", "savannah250xo"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "Adult_Forum",
        "uri_check" : "https://adultforum.gr/{account}-glamour-escorts/",
        "e_code" : 200,
        "e_string" : "Glamour Escorts ",
        "m_string" : "Page not found - Adult Forum Gr",
        "m_code" : 404,
        "known" : ["nastya3", "ekaterina"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "adultism",
        "uri_check" : "https://www.adultism.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "Last login:",
        "m_string" : "<title> Not Found",
        "m_code" : 404,
        "known" : ["laura", "sara"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "ADVFN",
        "uri_check" : "https://uk.advfn.com/forum/profile/{account}",
        "e_code" : 200,
        "e_string" :"Profile | ADVFN",
        "m_string" : "ADVFN ERROR - Page Not Found",
        "m_code" : 404,
        "known" : ["crypto", "crypto1"],
        "cat" : "finance"
       },
       {
        "name" : "Airline_Pilot_Life",
        "uri_check" : "https://airlinepilot.life/u/{account}.json",
        "uri_pretty" : "https://airlinepilot.life/u/{account}",
        "e_code" : 200,
        "e_string" : "primary_group_name",
        "m_string" : "he requested URL or resource could not be found.",
        "m_code" : 404,
        "known" : ["hannah", "addison"],
        "cat" : "social"
       },
       {
        "name" : "Airliners",
        "uri_check" : "https://www.airliners.net/user/{account}/profile",
        "e_code" : 200,
        "e_string" : "'s Profile | Airliners Members | Airliners.net",
        "m_string" : "An Error Occurred",
        "m_code" : 404,
        "known" : ["pilot", "pilota"],
        "cat" : "social"
       },
       {
        "name" : "akniga",
        "uri_check" : "https://akniga.org/profile/{account}",
        "e_code" : 200,
        "e_string" : " - Аудиокниги Клуб</title",
        "m_string" : "К сожалению, такой страницы не существует. Вероятно, она была удалена с сервера, либо ее здесь никогда не было.",
        "m_code" : 200,
        "known" : ["bob", "blue"],
        "cat" : "hobby"
       },
       {
        "name" : "Albicla",
        "uri_check" : "https://albicla.com/{account}/post/1",
        "uri_pretty" : "https://albicla.com/{account}",
        "e_code" : 500,
        "e_string" : "500 Post tymczasowo niedostępny",
        "m_string" : "404 Nie znaleziono użytkownika",
        "m_code" : 200,
        "known" : ["GazetaPolska", "GPCodziennie"],
        "cat" : "social"
       },
       {
        "name" : "alik",
        "uri_check" : "https://www.alik.cz/u/{account}",
        "e_code" : 200,
        "e_string" : "Vizitka – Alík.cz</title>",
        "m_string" : "<title>Vizitka nenalezena",
        "m_code" : 404,
        "known" : ["igor", "pavel"],
        "cat" : "social"
       },
       {
        "name" : "allmylinks",
        "uri_check" : "https://allmylinks.com/{account}",
        "e_code" : 200,
        "e_string" : "message",
        "m_string" : "Page not found",
        "m_code" : 404,
        "known" : ["blue", "goddessbecca"],
        "cat" : "social"
       },
       {
         "name" : "Alura",
         "uri_check" : "https://cursos.alura.com.br/user/{account}",
         "e_code" : 200,
         "e_string" : "Perfil de",
         "m_string" : "\"error\":\"Not Found\"",
         "m_code" : 404,
         "known" : ["edmilson", "jonathan"],
         "cat" : "tech"
       },
       {
        "name" : "Ameblo",
        "uri_check" : "https://ameblo.jp/{account}",
        "e_code" : 200,
        "e_string" : "画像一覧",
        "m_string" : "削除された可能性がございます。",
        "m_code" : 404,
        "known" : ["ereko-blog", "senpai"],
        "cat" : "blog"
       },
       {
        "name" : "AmericanThinker",
        "uri_check" : "https://www.americanthinker.com/author/{account}/",
        "e_code" : 200,
        "e_string" : "Articles &amp;",
        "m_string" : "American Thinker</title>",
        "m_code" : 301,
        "known" : ["terrypaulding", "monicashowalter"],
        "cat" : "political"
       },
       {
        "name" : "Anime-Planet",
        "uri_check" : "https://www.anime-planet.com/api/validation/username",
        "uri_pretty" : "https://www.anime-planet.com/users/{account}",
        "post_body" : "{\"username\":\"{account}\"}",
        "e_code" : 400,
        "e_string" : "\"status\":\"err\"",
        "m_string" : "\"status\":\"ok\"",
        "m_code" : 200,
        "known" : ["zala", "lindapearl"],
        "cat" : "social",
        "headers" : {
            "Content-Type": "application/json"
        },
        "protection" :  ["cloudflare"]
       },
       {
        "name" : "AniList",
        "uri_check" : "https://graphql.anilist.co",
        "uri_pretty" : "https://anilist.co/user/{account}",
        "post_body" : "{\"query\":\"query{User(name:\\\"{account}\\\"){id name}}\"}",
        "e_code" : 200,
        "e_string" : "\"id\":",
        "m_code" : 404,
        "m_string" : "Not Found",
        "known" : ["test", "johndoe"],
        "cat" : "social",
        "headers" : {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
       },
       {
        "name" : "anonup",
        "uri_check" : "https://anonup.com/@{account}",
        "e_code" : 200,
        "e_string" : "Show followings",
        "m_string" : "Page not found!",
        "m_code" : 302,
        "known" : ["john", "peter"],
        "cat" : "social"
       },
       {
        "name" : "Apex Legends",
        "uri_check" : "https://api.tracker.gg/api/v2/apex/standard/profile/origin/{account}",
        "uri_pretty" : "https://apex.tracker.gg/apex/profile/origin/{account}/overview",
        "headers" : {"User-Agent": "Mozilla/5.0 (Mozilla/5.0 (X11; Linux i686; rv:128.0) Gecko/20100101 Firefox/128.0", "Accept-Language": "en-US,en;q=0.5", "Origin": "https://apex.tracker.gg", "Referer": "https://apex.tracker.gg/", "TE": "trailers"},
        "e_code" : 200,
        "e_string" : "platformInfo",
        "m_code" : 404,
        "m_string" : "CollectorResultStatus::NotFound",
        "known" : ["tttcheekyttt", "RollsRoyce_Dawn"],
        "cat" : "gaming"
       },
       {
        "name" : "Appian",
        "uri_check" : "https://community.appian.com/members/{account}",
        "e_code" : 200,
        "e_string" : "User Profile",
        "m_string" : "Go back to our",
        "m_code" : 301,
        "known" : ["mikec", "varunkumarb0001"],
        "cat" : "tech"
       },
       {
        "name" : "Archive Of Our Own Account",
        "uri_check" : "https://archiveofourown.org/users/{account}",
        "e_code" : 200,
        "e_string" : "class=\"user home\"",
        "m_string" : "class=\"system errors error-404 region\"",
        "m_code" : 404,
        "known" : ["test", "john"],
        "cat" : "hobby"
       },
       {
        "name" : "Arduino",
        "uri_check" : "https://projecthub.arduino.cc/{account}",
        "e_code" : 200,
        "e_string" : "| Arduino Project Hub",
        "m_string" : "Arduino Project Hub",
        "m_code" : 404,
        "known" : ["peter", "john"],
        "cat" : "tech"
       },
       {
        "name" : "ArmorGames",
        "uri_check" : "https://armorgames.com/user/{account}",
        "e_code" : 200,
        "e_string" : "about",
        "m_string" : "404: Oh Noes!",
        "m_code" : 302,
        "known" : ["john", "sammy"],
        "cat" : "gaming"
       },
       {
        "name" : "ArtBreeder",
        "uri_check" : "https://www.artbreeder.com/{account}",
        "e_code" : 200,
        "e_string" : "<title>",
        "m_string" : "Not found:",
        "m_code" : 404,
        "known" : ["dolores", "cyborghyena"],
        "cat" : "art"
       },
       {
        "name" : "Artists & Clients",
        "uri_check" : "https://artistsnclients.com/people/{account}",
        "e_code" : 200,
        "e_string" : "Member Since",
        "m_code" : 404,
        "m_string" : "The page you requested wasn't there when we tried to get it for you. What a bother!",
        "known" : ["luluc0", "MuraArts"],
        "cat" : "art"
       },
       {
        "name" : "ArtStation",
        "uri_check" : "https://www.artstation.com/{account}",
        "e_code" : 200,
        "e_string" : "Portfolio",
        "m_code" : 404,
        "m_string" : "Page not found",
        "known" : ["kongaxl_design", "alex_pi"],
        "cat" : "art"
       },
       {
        "name" : "ArchWiki",
        "uri_check" : "https://wiki.archlinux.org/api.php?action=query&format=json&list=users&ususers={account}&usprop=cancreate&formatversion=2&errorformat=html&errorsuselocal=true&uselang=en",
        "uri_pretty" : "https://wiki.archlinux.org/title/User:{account}",
        "e_code" : 200,
        "e_string" : "\"userid\":",
        "m_string" : "\"missing\":true",
        "m_code" : 200,
        "known" : ["Lahwaacz", "Erus_Iluvatar"],
        "cat" : "social"
       },
       {
        "name" : "asciinema",
        "uri_check" : "https://asciinema.org/~{account}",
        "e_code" : 200,
        "e_string" : "s profile - asciinema",
        "m_string" : "This page doesn't exist. Sorry!",
        "m_code" : 404,
        "known" : ["john", "red"],
        "cat" : "coding"
       },
      {
        "name" : "AtCoder",
        "uri_check" : "https://atcoder.jp/users/{account}",
        "e_code" : 200,
        "e_string" : "<h3>Contest Status</h3>",
        "m_string" : ">404 Page Not Found</h1>",
        "m_code" : 404,
        "known" : ["apiad", "kotatsugame"],
        "cat" : "coding"
       },
       {
        "name" : "au.ru",
        "uri_check" : "https://au.ru/user/{account}/",
        "e_code" : 200,
        "e_string" : "Лоты пользователя ",
        "m_string" : "Пользователь не найден",
        "m_code" : 404,
        "known" : ["Svetlana7", "nastya"],
        "cat" : "misc"
       },
       {
        "name" : "Audiojungle",
        "uri_check" : "https://audiojungle.net/user/{account}",
        "e_code" : 200,
        "e_string" : "s profile on AudioJungle",
        "m_string" : "404 - Nothing to see here",
        "m_code" : 404,
        "known" : ["john", "reds"],
        "cat" : "music"
       },
       {
        "name" : "Avid Community",
        "uri_check" : "https://community.avid.com/members/{account}/default.aspx",
        "e_code" : 200,
        "e_string" : "My Activity",
        "m_code" : 302,
        "headers" : {"Host": "community.avid.com", "User-Agent": "Mozilla/5.0 (Mozilla/5.0 (X11; Linux i686; rv:128.0) Gecko/20100101 Firefox/128.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8", "Cache-Control": "no-cache"},
        "m_string" : "The user you requested cannot be found.",
        "known" : ["Thayne", "Admin"],
        "cat" : "music"
       },
       {
        "name" : "babepedia",
        "uri_check" : "https://www.babepedia.com/user/{account}",
        "e_code" : 200,
        "e_string" : "'s Page</title>",
        "m_string" : "Profile not found",
        "m_code" : 404,
        "known" : ["cherry", "betty"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "BabyPips",
        "uri_check" : "https://forums.babypips.com/u/{account}.json",
        "uri_pretty" : "https://forums.babypips.com/u/{account}/summary",
        "e_code" : 200,
        "e_string" : "user_badges",
        "m_string" : "The requested URL or resource could not be found",
        "m_code" : 404,
        "known" : ["baemax023", "scottycarsonmvp"],
        "cat" : "social"
       },
       {
        "name" : "Bandcamp",
        "uri_check" : "https://bandcamp.com/{account}",
        "e_code" : 200,
        "e_string" : " collection | Bandcamp</title>",
        "m_string" : "<h2>Sorry, that something isn’t here.</h2>",
        "m_code" : 404,
        "known" : ["alice", "bob"],
        "cat" : "music"
       },
       {
        "name" : "Bandlab",
        "uri_check" : "https://www.bandlab.com/api/v1.3/users/{account}",
        "uri_pretty" : "https://www.bandlab.com/{account}",
        "e_code" : 200,
        "e_string" : "about",
        "m_string" : "Couldn't find any matching element, it might be deleted",
        "m_code" : 404,
        "known" : ["rave_flawless", "delutaya"],
        "cat" : "music"
       },
       {
        "name" : "bblog_ru",
        "uri_check" : "https://www.babyblog.ru/user/{account}",
        "e_code" : 200,
        "e_string" : "@",
        "m_string" : "БэбиБлог - беременность, календарь беременности, дневники",
        "m_code" : 301,
        "known" : ["igor", "olga"],
        "cat" : "misc"
       },
       {
        "name" : "BDSMLR",
        "uri_check" : "https://{account}.bdsmlr.com",
        "strip_bad_char" : ".",
        "e_code" : 200,
        "e_string" : "login",
        "m_string" : "This blog doesn't exist.",
        "m_code" : 200,
        "known" : ["themunch", "shibari4all"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "bdsmsingles",
        "uri_check" : "https://www.bdsmsingles.com/members/{account}/",
        "e_code" : 200,
        "e_string" : "<title>Profile",
        "m_string" : "BDSM Singles",
        "m_code" : 302,
        "known" : ["GoddessBlueDiamo", "aalama"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "Beacons",
        "uri_check" : "https://beacons.ai/{account}",
        "e_code" : 200,
        "e_string" : " - Link in Bio &amp; Creator Tools | Beacons</title>",
        "m_string" : "The page you are looking for does not seem to exist anymore",
        "m_code" : 200,
        "known" : ["rafaballerini", "lexaloco", "jardred"],
        "cat" : "social",
        "protection" : ["cloudflare"]
       },
       {
        "name" : "Behance",
        "uri_check" : "https://www.behance.net/{account}",
        "e_code" : 200,
        "e_string" : "og:site_name",
        "m_string" : "<title>Oops!",
        "m_code" : 404,
        "known" : ["alice", "john"],
        "cat" : "business"
       },
       {
        "name" : "Bentbox",
        "uri_check" : "https://bentbox.co/{account}",
        "e_code" : 200,
        "e_string" : "<div id=\"user_bar\">",
        "m_string" : "This user is currently not available",
        "m_code" : 200,
        "known" : ["brockdoom", "witchhouse", "hotoptics"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "Bento",
        "uri_check" : "https://bento.me/{account}",
        "e_code" : 200,
        "e_string" : "href=\"https://bento.me/explore\"",
        "m_string" : ">Available!</div>",
        "m_code" : 404,
        "known" : ["carlito", "taylor"],
        "cat" : "social"
       },
       {
        "name" : "BiggerPockets",
        "uri_check" : "https://www.biggerpockets.com/users/{account}",
        "e_code" : 200,
        "e_string" : "| BiggerPockets</title>",
        "m_string" : "Page not found",
        "m_code" : 404,
        "known" : ["trustgreene", "chasel9"],
        "cat" : "finance"
       },
       {
        "name" : "BIGO Live",
        "uri_check" : "https://www.bigo.tv/user/{account}",
        "e_code" : 200,
        "e_string" : "userInfo:{nickName",
        "m_string" : "userInfo:{}",
        "m_code" : 200,
        "known" : ["treasdior", "Jacin19"],
        "cat" : "gaming"
       },
       {
        "name" : "Bikemap",
        "uri_check" : "https://www.bikemap.net/en/u/{account}/routes/created/",
        "e_code" : 200,
        "e_string" : "- 🚲 Bikemap</title>",
        "m_string" : "<title>Page not found - Error 404 ",
        "m_code" : 404,
        "known" : ["mike", "greg"],
        "cat" : "health"
       },
       {
        "name" : "Bimpos",
        "uri_check" : "https://ask.bimpos.com/user/{account}",
        "e_code" : 200,
        "e_string" : "<title>User ",
        "m_string" : "Page not found",
        "m_code" : 404,
        "known" : ["john", "db"],
        "cat" : "tech"
       },
       {
        "name" : "biolink",
        "uri_check" : "https://bio.link/{account}",
        "e_code" : 200,
        "e_string" : "profile:username",
        "m_string" : "The page you’re looking for doesn’t exist",
        "m_code" : 404,
        "known" : ["adli_hm", "jake"],
        "cat" : "misc"
       },
       {
        "name" : "Bio Sites",
        "uri_check" : "https://bio.site/{account}",
        "e_code" : 200,
        "e_string" : "section\":{\"handles",
        "m_string" : "This site no longer exists",
        "m_code" : 404,
        "known" : ["leticiabufoni", "kayurkaRhea"],
        "cat" : "social"
       },
       {
        "name" : "Bitbucket",
        "uri_check" : "https://bitbucket.org/!api/2.0/repositories/{account}?page=1&pagelen=25&sort=-updated_on&q=&fields=-values.owner%2C-values.workspace",
        "uri_pretty" : "https://bitbucket.org/{account}/workspace/repositories/",
        "e_code" : 200,
        "e_string" : "full_name",
        "m_string" : "No workspace with identifier",
        "m_code" : 404,
        "known" : ["LaNMaSteR53", "osamahalisawi"],
        "cat" : "coding"
       },
       {
        "name" : "Bitchute",
        "uri_check" : "https://api.bitchute.com/api/beta/channel",
        "uri_pretty" : "https://www.bitchute.com/channel/{account}/",
        "post_body" : "{\"channel_id\":\"{account}\"}",
        "e_code" : 200,
        "e_string" : "\"channel_id\":",
        "m_string" : "\"errors\":",
        "m_code" : 404,
        "known" : ["simon_parkes", "americafloats", "daindor"],
        "cat" : "political",
        "headers" : {
            "Content-Type": "application/json"
        }
       },
       {
        "name" : "Blogger",
        "uri_check" : "https://www.blogger.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "shadow-light user-stats",
        "m_string" : "Sorry, the blog you were looking for does not exist.",
        "m_code" : 405,
        "known" : ["07333944864481878697", "05941544278367416980"],
        "cat" : "blog"
       },
       {
        "name" : "blogi.pl",
        "uri_check" : "https://www.blogi.pl/osoba,{account}.html",
        "e_code" : 200,
        "e_string" : "Informacje ogólne",
        "m_string" : "Niepoprawny adres.",
        "m_code" : 200,
        "known" : ["naukowa", "izkpaw"],
        "cat" : "blog"
       },
       {
        "name" : "Blogmarks",
        "uri_check" : "http://blogmarks.net/user/{account}",
        "e_code" : 200,
        "e_string" : "class=\"mark\"",
        "m_string" : "",
        "m_code" : 200,
        "known" : ["test", "mike"],
        "cat" : "misc"
       },
       {
        "name" : "Blogspot",
        "uri_check" : "http://{account}.blogspot.com",
        "strip_bad_char" : ".",
        "e_code" : 200,
        "e_string" : "Blogger Template Style",
        "m_string" : "Blog not found",
        "m_code" : 404,
        "known" : ["test"],
        "cat" : "blog"
       },
       {
        "name" : "Bluesky 1",
        "uri_check" : "https://bsky.app/profile/{account}",
        "e_code" : 200,
        "e_string" : "on Bluesky",
        "m_code" : 200,
        "m_string" : "<p id=\"bsky_did\"></p>",
        "known" : ["bsky.app", "safety.bsky.app"],
        "cat" : "social"
       },
       {
         "name" : "Bluesky 2",
         "uri_check" : "https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor={account}.bsky.social",
         "uri_pretty" : "https://bsky.app/profile/{account}.bsky.social",
         "e_code" : 200,
         "e_string" : "\"handle\":\"",
         "m_code" : 400,
         "m_string" : "\"message\":\"Profile not found\"",
         "known" : ["john", "mark"],
         "cat" : "social"
       },
       {
        "name" : "BoardGameGeek",
        "uri_check" : "https://api.geekdo.com/api/accounts/validate/username?username={account}",
        "uri_pretty" : "https://boardgamegeek.com/user/{account}",
        "e_code" : 200,
        "e_string" : "\"isValid\":false",
        "m_string" : "\"isValid\":true",
        "m_code" : 200,
        "known" : ["ntrautner", "Petdoc"],
        "cat" : "gaming"
       },
       {
        "name" : "BodyBuilding.com",
        "uri_check" : "http://api.bodybuilding.com/api-proxy/bbc/get?slug={account}",
        "uri_pretty" : "http://bodyspace.bodybuilding.com/{account}/",
        "e_code" : 200,
        "e_string" : "username",
        "m_string" : "data\" :\"\"",
        "m_code" : 200,
        "known" : ["mike"],
        "cat" : "health"
       },
       {
        "name" : "bonga_cams",
        "uri_check" : "https://pt.bongacams.com/{account}",
        "e_code" : 200,
        "e_string" : "Chat público ao vivo de",
        "m_string" : "Câmaras de sexo free: chat pornô ao vivo",
        "m_code" : 404,
        "known" : ["prettykatea", "milaowens"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "Bookcrossing",
        "uri_check" : "https://www.bookcrossing.com/mybookshelf/{account}",
        "e_code" : 200,
        "e_string" : "Recent Book Activity",
        "m_string" : "Sorry, we were unable to locate the content that you requested.",
        "m_code" : 404,
        "known" : ["john", "bob"],
        "cat" : "hobby"
       },
       {
        "name" : "boosty",
        "uri_check" : "https://boosty.to/{account}",
        "e_code" : 200,
        "e_string" : "- exclusive content on Boosty</title>",
        "m_string" : "Blog not found",
        "m_code" : 200,
        "known" : ["evdokia", "lana"],
        "cat" : "social"
       },
       {
        "name" : "Booth",
        "uri_check" : "https://{account}.booth.pm/",
        "strip_bad_char" : ".",
        "e_code" : 200,
        "e_string" : "- BOOTH</title>",
        "m_string" : "BOOTH - The International Indie Art Marketplace",
        "m_code" : 302,
        "known" : ["monoliorder", "hasya"],
        "cat" : "shopping"
       },
       {
        "name" : "Brickset",
        "uri_check" : "https://brickset.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "Member since:</dt>",
        "m_string" : "{name}</h1>",
        "m_code" : 200,
        "known" : ["lowlead", "vwong19"],
        "cat" : "hobby"
       },
       {
        "name" : "BugCrowd",
        "uri_check" : "https://bugcrowd.com/{account}/profile_widgets",
        "uri_pretty" : "https://bugcrowd.com/{account}",
        "e_code" : 200,
        "e_string" : "\"widgets\":",
        "m_string" : "class='cc-error-page__msg'",
        "m_code" : 404,
        "known" : ["lopseg", "Ebrietas"],
        "cat" : "tech"
       },
       {
        "name" : "Bunpro",
        "uri_check" : "https://community.bunpro.jp/u/{account}.json",
        "e_code" : 200,
        "e_string" : "username",
        "m_code" : 404,
        "m_string" : "The requested URL or resource could not be found.",
        "known" : ["blacktide", "honey"],
        "cat" : "social"
       },
       {
        "name" : "Buy Me a Coffee",
        "uri_check" : "https://app.buymeacoffee.com/api/v1/check_availability",
        "uri_pretty" : "https://buymeacoffee.com/{account}",
        "post_body" : "{\"project_slug\":\"{account}\"}",
        "e_code" : 200,
        "e_string" : "\"available\":false",
        "m_string" : "\"available\":true",
        "m_code" : 200,
        "known" : ["freebird", "robinwong"],
        "cat" : "finance",
        "protection" : ["cloudflare"],
        "headers" : {
            "Content-Type": "application/json"
        }
       },
       {
        "name" : "BuzzFeed",
        "uri_check" : "https://www.buzzfeed.com/{account}",
        "e_code" : 200,
        "e_string" : " on BuzzFeed</title><meta",
        "m_string" : "We can't find the page you're looking for",
        "m_code" : 404,
        "known" : ["janelytvynenko", "RobertK"],
        "cat" : "social"
       },
       {
        "name" : "cafecito",
        "uri_check" : "https://cafecito.app/{account}",
        "e_code" : 200,
        "e_string" : " | Cafecito</title>",
        "m_string" : "Es posible que el enlace que seleccionaste esté roto o que se haya eliminado la página",
        "m_code" : 404,
        "known" : ["braftty", "guillermo"],
        "cat" : "misc"
       },
       {
        "name" : "Calendy",
        "uri_check" : "https://calendly.com/{account}",
        "e_code" : 200,
        "e_string" : "og:author",
        "m_code" : 404,
        "m_string" : "Sorry, but the page you were looking for could not be found.",
        "known" : ["honey", "roger"],
        "cat" : "misc"
       },
       {
        "name" : "Cameo",
        "uri_check" : "https://www.cameo.com/{account}",
        "e_code" : 200,
        "e_string" : "aggregateRating",
        "m_string" : "",
        "m_code" : 301,
        "known" : ["michael_owen10", "sarahall3"],
        "cat" : "shopping"
       },
       {
        "name" : "Carbonmade",
        "uri_check" : "https://{account}.carbonmade.com/",
        "strip_bad_char" : ".",
        "e_code" : 200,
        "e_string" : "s online portfolio",
        "m_string" : "site not found",
        "m_code" : 404,
        "known" : ["jenny", "bob"],
        "cat" : "hobby"
       },
       {
        "name" : "Career.habr",
        "uri_check" : "https://career.habr.com/{account}",
        "e_code" : 200,
        "e_string" : "— Хабр Карьера</title>",
        "m_string" : "Ошибка 404",
        "m_code" : 404,
        "known" : ["alex", "bob"],
        "cat" : "business"
       },
       {
        "name" : "carrd.co",
        "uri_check" : "https://{account}.carrd.co",
        "strip_bad_char" : ".",
        "e_code" : 200,
        "e_string" : "( Made with Carrd )",
        "m_code" : 404,
        "m_string" : "Sorry, the requested page could not be found.",
        "known" : ["liam", "peter"],
        "cat" : "business"
       },
       {
        "name" : "CastingCallClub",
        "uri_check" : "https://www.castingcall.club/{account}",
        "e_code" : 200,
        "e_string" : "| Casting Call Club",
        "m_code" : 302,
        "m_string" : "404: This is not the page you were looking for. In the future, our AI robot overlords will be able to better predict exactly what you were looking for.",
        "known" : ["Lindz", "Danye"],
        "cat" : "hobby"
       },
       {
        "name" : "CD-Action",
        "uri_check" : "https://cdaction.pl/uzytkownicy/{account}",
        "e_code" : 200,
        "e_string" : "Lista gier:",
        "m_string" : "Coś się popsuło...",
        "m_code" : 404,
        "known" : ["saczuan", "cormac"],
        "cat" : "gaming"
       },
       {
        "name" : "cda.pl",
        "uri_check" : "https://www.cda.pl/{account}",
        "e_code" : 200,
        "e_string" : "Foldery",
        "m_string" : "Strona na którą chcesz wejść nie istnieje",
        "m_code" : 200,
        "known" : ["test2", "janek"],
        "cat" : "video"
       },
       {
        "name" : "cfx.re",
        "uri_check" : "https://forum.cfx.re/u/{account}.json",
        "uri_pretty" : "https://forum.cfx.re/u/{account}/summary",
        "e_code" : 200,
        "e_string" : "created_at",
        "m_string" : "The requested URL or resource could not be found.",
        "m_code" : 404,
        "known" : ["masiball", "anel_hadzyc", "kiminaze"],
        "cat" : "gaming"
       },
       {
        "name" : "championat",
        "uri_check" : "https://www.championat.com/user/{account}/",
        "e_code" : 200,
        "e_string" : "Личный профил",
        "m_string" : "Извините, запрашиваемая страница не найдена",
        "m_code" : 404,
        "known" : ["john", "bob"],
        "cat" : "news"
       },
       {
        "name" : "chatango.com",
        "uri_check" : "https://{account}.chatango.com",
        "e_code" : 200,
        "e_string" : "<title>Chatango!",
        "m_string" : "<title>Unknown User!",
        "m_code" : 200,
        "known" : ["7nights", "merbailey", "steakomura", "equicentric"],
        "cat" : "social"
       },
       {
        "name" : "Mastodon-Chaos.social",
        "uri_check" : "https://chaos.social/@{account}",
        "e_code" : 200,
        "e_string" : "@chaos.social) - chaos.social</title>",
        "m_string" : "The page you are looking for isn&#39;t here.",
        "m_code" : 404,
        "known" : ["dictvm", "sml"],
        "cat" : "social"
       },
       {
        "name" : "chaturbate",
        "uri_check" : "https://chaturbate.com/{account}/",
        "e_code" : 200,
        "e_string" : "'s Bio and Free Webcam",
        "m_string" : "It's probably just a broken link",
        "m_code" : 404,
        "known" : ["pussylovekate", "kemii"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "cHEEZburger",
        "uri_check" : "https://profile.cheezburger.com/{account}",
        "e_code" : 200,
        "e_string" : "profile-header",
        "m_string" : "<title>Home - ",
        "m_code" : 302,
        "known" : ["john"],
        "cat" : "hobby"
       },
       {
        "name" : "Chamsko",
        "uri_check" : "https://www.chamsko.pl/profil/{account}",
        "e_code" : 200,
        "e_string" : "W serwisie od",
        "m_string" : "Strona nie istnieje.",
        "m_code" : 404,
        "known" : ["test", "janek"],
        "cat" : "images"
       },
       {
        "name" : "Chess.com",
        "uri_check" : "https://api.chess.com/pub/player/{account}",
        "uri_pretty" : "https://www.chess.com/member/{account}",
        "e_code" : 200,
        "e_string" : "player_id",
        "m_string" : "not found",
        "m_code" : 404,
        "known" : ["john", "peter", "josh"],
        "cat" : "gaming"
       },
       {
        "name" : "Chomikuj.pl",
        "uri_check" : "https://chomikuj.pl/{account}/",
        "e_code" : 200,
        "e_string" : "Foldery",
        "m_string" : "Chomik o takiej nazwie nie istnieje",
        "m_code" : 404,
        "known" : ["test", "test2"],
        "cat" : "misc"
       },
       {
        "name" : "Chyoa",
        "uri_check" : "https://chyoa.com/user/{account}",
        "e_code" : 200,
        "e_string" : "When I'm not reading erotica I like to read",
        "m_string" : "Sorry, I got distracted...",
        "m_code" : 404,
        "known" : ["joe", "carlos01"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "Climatejustice.rocks (Mastodon Instance)",
        "uri_check" : "https://climatejustice.rocks/api/v1/accounts/lookup?acct={account}",
        "uri_pretty" : "https://climatejustice.rocks/@{account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_code" : 404,
        "m_string" : "Record not found",
        "known" : ["paula", "ClimbitJustice"],
        "cat" : "social"
       },
       {
        "name" : "Cloudflare",
        "uri_check" : "https://community.cloudflare.com/u/{account}/card.json",
        "uri_pretty" : "https://community.cloudflare.com/u/{account}",
        "e_code" : 200,
        "e_string" : "user_avatar",
        "m_string" : "The requested URL or resource could not be found",
        "m_code" : 404,
        "known" : ["carl", "morten"],
        "cat" : "tech"
      },
       {
        "name" : "Clubhouse",
        "uri_check" : "https://www.clubhouse.com/@{account}",
        "e_code" : 200,
        "e_string" : "\"user\":",
        "m_string" : "404",
        "m_code" : 404,
        "known" : ["kirbyplessas", "rohan"],
        "cat" : "social"
       },
       {
        "name" : "cnet",
        "uri_check" : "https://www.cnet.com/profiles/{account}/",
        "e_code" : 200,
        "e_string" : "Member Since:",
        "m_string" : "Page Not Found (404) - CNET",
        "m_code" : 301,
        "known" : ["john", "bob"],
        "cat" : "news"
       },
       {
        "name" : "Community Adobe",
        "uri_check" : "https://community.adobe.com/t5/forums/searchpage/tab/user?q={account}",
        "e_code" : 200,
        "e_string" : "UserSearchItemContainer",
        "m_string" : "No search results found.",
        "m_code" : 200,
        "known" : ["test", "janet"],
        "cat" : "tech"
       },
       {
        "name" : "Coda",
        "uri_check" : "https://coda.io/@{account}/",
        "e_code" : 200,
        "e_string" : "- Coda Profile</title>",
        "m_string" : "<title>Coda | Page not found - Coda</title>",
        "m_code" : 404,
        "known" : ["huizer", "kennywong"],
        "cat" : "hobby"
       },
       {
        "name" : "Codeberg",
        "uri_check" : "https://codeberg.org/{account}",
        "e_code" : 200,
        "e_string" : "Joined on",
        "m_code" : 404,
        "m_string" : "The page you are trying to reach either",
        "known" : ["dachary", "happy"],
        "cat" : "coding"
       },
       {
        "name" : "Codecademy",
        "uri_check" : "https://discuss.codecademy.com/u/{account}/summary",
        "e_code" : 200,
        "e_string" : "<title>  Profile - ",
        "m_string" : "Oops! That page doesn’t exist",
        "m_code" : 404,
        "known" : ["doctypeme", "ocean.war"],
        "cat" : "coding"
       },
       {
        "name" : "CodeChef",
        "uri_check" : "https://www.codechef.com/users/{account}",
        "e_code" : 200,
        "e_string" : "class=\"user-profile-container\"",
        "m_string" : "",
        "m_code" : 302,
        "known" : ["maroonrk", "lyrically"],
        "cat" : "coding"
       },
       {
        "name" : "Codeforces",
        "uri_check" : "https://codeforces.com/api/user.info?handles={account}",
        "uri_pretty" : "https://codeforces.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "\"status\":\"OK\"",
        "m_string" : "\"status\":\"FAILED\"",
        "m_code" : 400,
        "known" : ["Abdul01", "Abdullah"],
        "cat" : "coding"
       },
       {
        "name" : "codementor",
        "uri_check" : "https://www.codementor.io/@{account}",
        "e_code" : 200,
        "e_string" : "ABOUT ME",
        "m_string" : "404/favicon.png",
        "m_code" : 404,
        "known" : ["e4c5", "juanelfers"],
        "cat" : "coding"
       },
       {
        "name" : "Code Project",
        "uri_check" : "https://www.codeproject.com/Members/{account}",
        "e_code" : 200,
        "e_string" : "Member since",
        "m_string" : "Unable to load the requested member's information",
        "m_code" : 200,
        "known" : ["WmCraig", "Rick-York"],
        "cat" : "coding"
       },
       {
        "name" : "Codewars",
        "uri_check" : "https://www.codewars.com/users/{account}",
        "e_code" : 200,
        "e_string" : "| Codewars",
        "m_string" : "Whoops! The page you were looking for doesn't seem to exist.",
        "m_code" : 404,
        "known" : ["john", "reds"],
        "cat" : "coding"
       },
       {
        "name" : "Coderwall",
        "uri_check" : "https://coderwall.com/{account}/",
        "e_code" : 200,
        "e_string" : "s profile |",
        "m_string" : "404! Our feels when that url is used",
        "m_code" : 404,
        "known" : ["john", "test"],
        "cat" : "coding"
       },
       {
        "name" : "COLOURlovers",
        "uri_check" : "https://www.colourlovers.com/lover/{account}",
        "e_code" : 200,
        "e_string" : "Color lovin' since",
        "m_string" : "Lover has gone missing",
        "m_code" : 410,
        "known" : ["amorremanet", "bezzalopoly"],
        "cat" : "hobby"
       },
       {
        "name" : "contactos.sex",
        "uri_check" : "https://www.contactossex.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "Información Personal",
        "m_string" : "Desde 2001 conectando gente!",
        "m_code" : 302,
        "known" : ["danijak", "darkfox"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "coroflot",
        "uri_check" : "https://www.coroflot.com/{account}",
        "e_code" : 200,
        "e_string" : "portfolio",
        "m_string" : "Looking for something?",
        "m_code" : 404,
        "known" : ["john", "blue"],
        "cat" : "art"
       },
       {
        "name" : "cowboys4angels",
        "uri_check" : "https://cowboys4angels.com/cowboy/{account}/",
        "e_code" : 200,
        "e_string" : " - Cowboys 4 Angels</title>",
        "m_string" : "Error Page not found",
        "m_code" : 404,
        "known" : ["jaxjames", "jordan-2"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "cracked_io",
        "uri_check" : "https://cracked.io/{account}",
        "e_code" : 200,
        "e_string" : "Cracked.io - Profile of",
        "m_string" : "The member you specified is either invalid or doesn't exist",
        "m_code" : 404,
        "known" : ["RealPsycho", "SamWinchester"],
        "cat" : "social"
       },
       {
        "name" : "Cracked",
        "uri_check" : "https://www.cracked.com/members/{account}",
        "e_code" : 200,
        "e_string" : "Member Since",
        "m_string" : "",
        "m_code" : 302,
        "known" : ["mbattagl","Hatchback"],
        "cat" : "social"
       },
       {
        "name" : "crevado",
        "uri_check" : "https://{account}.crevado.com/",
        "strip_bad_char" : ".",
        "e_code" : 200,
        "e_string" : "Portfolio",
        "m_string" : "Site not found :-(",
        "m_code" : 404,
        "known" : ["john", "red"],
        "cat" : "images"
       },
       {
        "name" : "crowdin",
        "uri_check" : "https://crowdin.com/profile/{account}",
        "e_code" : 200,
        "e_string" : ") – Crowdin",
        "m_string" : "Page Not Found - Crowdin",
        "m_code" : 404,
        "known" : ["alex", "peter"],
        "cat" : "hobby"
       },
       {
        "name" : "Cults3D",
        "uri_check" : "https://cults3d.com/en/users/{account}/creations",
        "e_code" : 200,
        "e_string" : "All the 3D models of",
        "m_string" : "Oh dear, this page is not working!",
        "m_code" : 404,
        "known" : ["Bstar3Dart", "john"],
        "cat" : "hobby"
       },
       {
        "name" : "Curiouscat",
        "uri_check" : "https://curiouscat.live/api/v2.1/profile?username={account}",
        "uri_pretty" : "https://curiouscat.live/{account}",
        "e_code" : 200,
        "e_string" : "is_followed_by_me",
        "m_code" : 200,
        "m_string" : "\"error\": 404",
        "known" : ["kindokja9158", "saki"],
        "cat" : "social"
       },
       {
        "name" : "Cytoid",
        "uri_check" : "https://cytoid.io/profile/{account}",
        "e_code" : 200,
        "e_string" : "Joined",
        "m_code" : 404,
        "m_string" : "Profile not found",
        "known" : ["nyala", "speedymlg7"],
        "cat" : "gaming"
       },
       {
        "name" : "darudar",
        "uri_check" : "https://darudar.org/users/{account}/",
        "e_code" : 200,
        "e_string" : ". Дарудар",
        "m_string" : "404. Дару~дар: миру~мир!",
        "m_code" : 404,
        "known" : ["svetlana7", "igor"],
        "cat" : "misc"
       },
       {
        "name" : "datezone",
        "uri_check" : "https://www.datezone.com/users/{account}/",
        "e_code" : 200,
        "e_string" : "profile_status",
        "m_string" : "404: page not found",
        "m_code" : 200,
        "known" : ["maniektwist","carllos"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "dateinasia",
        "uri_check" : "https://www.dateinasia.com/{account}",
        "e_code" : 200,
        "e_string" : "About me",
        "m_string" : "The page you are looking for does not exist",
        "m_code" : 404,
        "known" : ["shime", "janeferater"],
        "cat" : "dating"
       },
       {
        "name" : "Dating.ru",
        "uri_check" : "https://dating.ru/{account}/",
        "e_code" : 200,
        "e_string" : "| dating.ru",
        "m_string" : "Такой страницы не существует.",
        "m_code" : 404,
        "known" : ["john", "blue"],
        "cat" : "dating"
       },
       {
        "name" : "Mastodon-Defcon",
        "uri_check" : "https://defcon.social/@{account}",
        "e_code" : 200,
        "e_string" : "- DEF CON Social</title>",
        "m_string" : "The page you are looking for isn&#39;t here.",
        "m_code" : 404,
        "known" : ["defcon", "buttersnatcher"],
        "cat" : "social"
       },
       {
        "name" : "Demotywatory",
        "uri_check" : "https://demotywatory.pl/user/{account}",
        "e_code" : 200,
        "e_string" : "Z nami od:",
        "m_string" : "Użytkownik o podanym pseudonimie nie istnieje.",
        "m_code" : 200,
        "known" : ["test", "test2"],
        "cat" : "images"
       },
       {
        "name" : "depop",
        "uri_check" : "https://www.depop.com/{account}/",
        "e_code" : 200,
        "e_string" : "s Shop - Depop",
        "m_string" : "Sorry, that page doesn't exist",
        "m_code" : 404,
        "known" : ["sara", "susan"],
        "cat" : "shopping"
       },
       {
        "name" : "Designspriation",
        "uri_check" : "https://www.designspiration.com/{account}/",
        "e_code" : 200,
        "e_string" : "has discovered on Designspiration",
        "m_string" : "Content Not Found",
        "m_code" : 404,
        "known" : ["sam", "smith"],
        "cat" : "art"
       },
       {
        "name" : "Destructoid",
        "uri_check" : "https://www.destructoid.com/?name={account}",
        "e_code" : 200,
        "e_string" : "Follow",
        "m_string" : "Error in query",
        "m_code" : 200,
        "known" : ["john", "alice", "bob"],
        "cat" : "social"
       },
       {
        "name" : "DeviantArt",
        "uri_check" : "https://www.deviantart.com/{account}",
        "e_code" : 200,
        "e_string" : " | DeviantArt</title>",
        "m_string" : "DeviantArt: 404",
        "m_code" : 404,
        "known" : ["rattybike", "john"],
        "cat" : "images"
       },
       {
        "name" : "dev.to",
        "uri_check" : "https://dev.to/{account}",
        "e_code" : 200,
        "e_string" : "- DEV",
        "m_string" : "This page does not exist",
        "m_code" : 301,
        "known" : ["john", "bob"],
        "cat" : "coding"
       },
       {
        "name" : "devRant",
        "uri_check" : "https://devrant.com/users/{account}",
        "e_code" : 200,
        "e_string" : "Joined devRant on",
        "m_string" : "<!-- row start signup -->",
        "m_code" : 302,
        "known" : ["dfox", "trogus"],
        "cat" : "coding"
       },
       {
        "name" : "dfgames",
        "uri_check" : "https://www.dfgames.com.br/user/{account}",
        "e_code" : 200,
        "e_string" : "Reputa",
        "m_string" : "404 Not Found",
        "m_code" : 404,
        "known" : ["carlos01", "eduardo"],
        "cat" : "gaming"
       },
       {
        "name" : "Diablo",
        "uri_check" : "https://diablo2.io/member/{account}/",
        "e_code" : 200,
        "e_string" :"Viewing profile - ",
        "m_string" : "The requested user does not exist",
        "m_code" : 404,
        "known" : ["Mike01", "John"],
        "cat" : "gaming"
       },
       {
        "name" : "diigo",
        "uri_check" : "https://www.diigo.com/interact_api/load_profile_info?name={account}",
        "uri_pretty" : "https://www.diigo.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "regist_at",
        "m_string" : "{}",
        "m_code" : 200,
        "known" : ["whoami", "johndoe"],
        "cat" : "images"
       },
       {
       "name" : "DIBIZ",
        "uri_check" : "https://www.dibiz.com/{account}",
        "e_code" : 200,
        "e_string" : "Add to contacts</span>",
        "m_string" : "An Error Has Occurred",
        "m_code" : 404,
        "known" : ["fractalhue", "rid"],
        "cat" : "business"
       },
       {
        "name" : "Digitalspy",
        "uri_check" : "https://forums.digitalspy.com/profile/discussions/{account}",
        "e_code" : 200,
        "e_string" : "About",
        "m_string" : "User not found",
        "m_code" : 404,
        "known" : ["JeffG1", "Maxatoria"],
        "cat" : "social"
       },
       {
        "name" : "Discogs",
        "uri_check" : "https://api.discogs.com/users/{account}",
        "pretty_uri" : "https://www.discogs.com/user/{account}",
        "e_code" : 200,
        "e_string" : "\"id\"",
        "m_code" : 404,
        "m_string" : "User does not exist",
        "known" : ["damiano84", "bernadette69"],
        "cat" : "music"
       },
       {
        "name" : "Discourse",
        "uri_check" : "https://meta.discourse.org/u/{account}/summary.json",
        "uri_pretty" : "https://meta.discourse.org/u/{account}",
        "e_code" : 200,
        "e_string" : "topics",
        "m_code" : 404,
        "m_string" : "The requested URL or resource could not be found.",
        "known" : ["ndalliard", "gerhard"],
        "cat" : "misc"
       },
       {
        "name" : "discuss.elastic.co",
        "uri_check" : "https://discuss.elastic.co/u/{account}",
        "e_code" : 200,
        "e_string" : "<title>  Profile",
        "m_string" : "Oops!",
        "m_code" : 404,
        "known" : ["whoami", "johndoe"],
        "cat" : "tech"
       },
       {
        "name" : "Dissenter",
        "uri_check" : "https://dissenter.com/user/{account}",
        "e_code" : 200,
        "e_string" : "Dissenter | The Comment Section of the Internet",
        "m_string" : "That user is not registered here.",
        "m_code" : 404,
        "known" : ["pryerlee", "archdukeofevil"],
        "cat" : "political"
       },
       {
        "name" : "Disqus",
        "uri_check" : "https://disqus.com/by/{account}/",
        "e_code" : 200,
        "e_string" : "<title>Disqus Profile",
        "m_string" : "Page not found (404) - Disqus",
        "m_code" : 404,
        "known" : ["Aristotelian1", "50calibercat"],
        "cat" : "social"
       },
       {
        "name" : "DockerHub",
        "uri_check" : "https://hub.docker.com/v2/users/{account}/",
        "e_code" : 200,
        "e_string" : "uuid",
        "m_string" : "User not found",
        "m_code" : 404,
        "known" : ["bitnami", "torvalds"],
        "cat" : "coding"
       },
       {
        "name" : "Donation Alerts",
        "uri_check" : "https://www.donationalerts.com/api/v1/user/{account}/donationpagesettings",
        "uri_pretty" : "https://www.donationalerts.com/r/{account}",
        "e_code" : 200,
        "e_string" : "background_image_url",
        "m_code" : 202,
        "m_string" : "does not exist",
        "known" : ["gorou", "saku"],
        "cat" : "business"
       },
       {
        "name" : "dot.cards",
        "uri_check" : "https://dot.cards/{account}",
        "e_code" : 200,
        "e_string" : "status\": \"success",
        "m_string" : "status\": \"username_not_found",
        "m_code" : 200,
        "known" : ["dakmusic", "jhartwell"],
        "cat" : "business"
       },
       {
        "name" : "Dojoverse",
        "uri_check" : "https://dojoverse.com/members/{account}/",
        "e_code" : 200,
        "e_string" : "Joined",
        "m_string" : "Looks like you got lost!.",
        "m_code" : 404,
        "known" : ["eric", "danielrivera10927"],
        "cat" : "hobby"
       },
       {
        "name" : "Dribbble",
        "uri_check" : "https://dribbble.com/{account}",
        "e_code" : 200,
        "e_string" : " | Dribbble",
        "m_string" : "(404)</title>",
        "m_code" : 404,
        "known" : ["UI8", "keeplegend"],
        "cat" : "art"
       },
       {
        "name" : "Droners",
        "uri_check" : "https://droners.io/accounts/{account}/",
        "e_code" : 200,
        "e_string" : "- Professional Drone Pilot",
        "m_string" : "(404)</title>",
        "m_code" : 302,
        "known" : ["chriskahn", "swilken"],
        "cat" : "hobby"
       },
       {
        "name" : "Drum",
        "uri_check" : "https://drum.io/{account}/",
        "e_code" : 200,
        "e_string" : "firstName\": \"",
        "m_string" : "Page not found",
        "m_code" : 302,
        "known" : ["huckcredibleshotz", "thesuccesspalette"],
        "cat" : "hobby"
       },
       {
        "name" : "Duolingo",
        "uri_check" : "https://www.duolingo.com/2017-06-30/users?username={account}&_=1628308619574",
        "uri_pretty" : "https://www.duolingo.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "joinedClassroomIds",
        "m_string" : "\"users\" : []",
        "m_code" : 200,
        "known" : ["sdfsdf", "duolingo"],
        "cat" : "hobby"
       },
       {
        "name" : "easyen",
        "uri_check" : "https://easyen.ru/index/8-0-{account}",
        "e_code" : 200,
        "e_string" : "День рождения",
        "m_string" : "Пользователь не найден",
        "m_code" : 200,
        "known" : ["wd"],
        "cat" : "social"
       },
       {
        "name" : "eBay",
        "uri_check" : "https://www.ebay.com/usr/{account}",
        "e_code" : 200,
        "e_string" : "on eBay</title>",
        "m_string" : "The User ID you entered was not found",
        "m_code" : 200,
        "known" : ["the_gqs", "johnny"],
        "cat" : "shopping"
       },
       {
        "name" : "ebay_stores",
        "uri_check" : "https://www.ebay.com/str/{account}",
        "e_code" : 200,
        "e_string" : "| eBay Stores</title>",
        "m_string" : "Sorry, this store was not found.",
        "m_code" : 410,
        "known" : ["tactical", "tactical-security"],
        "cat" : "shopping"
       },
       {
        "name" : "Engadget",
        "uri_check" : "https://www.engadget.com/about/editors/{account}/",
        "e_code" : 200,
        "e_string" : "- Engadget</title>",
        "m_string" : "<title>,  -",
        "m_code" : 404,
        "known" : ["devindra-hardawar", "kris-holt"],
        "cat" : "tech"
       },
       {
        "name" : "EPORNER",
        "uri_check" : "https://www.eporner.com/profile/{account}/",
        "e_code" : 200,
        "e_string" : "Video/Pics views",
        "m_string" : "Profile not found",
        "m_code" : 404,
        "known" : ["LAM_2030", "DianaX814"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "Etsy",
        "uri_check" : "https://www.etsy.com/people/{account}",
        "e_code" : 200,
        "e_string" : " favorite items - Etsy</title>",
        "m_string" : "Sorry, the member you are looking for does not exist",
        "m_code" : 404,
        "known" : ["david", "happiness"],
        "cat" : "shopping"
       },
       {
        "name" : "Mastodon-EU_Voice",
        "uri_pretty" : "https://social.network.europa.eu/@{account}",
        "uri_check" : "https://social.network.europa.eu/api/v1/accounts/lookup?acct={account}",
        "e_code" : 200,
        "e_string" : "social.network.europa.eu",
        "m_string" : "The page you are looking for isn&#39;t here.",
        "m_code" : 404,
        "known" : ["EC_DIGIT", "EUSPA"],
        "cat" : "social"
       },
       {
        "name" : "Expressional.social (Mastodon Instance)",
        "uri_check" : "https://expressional.social/api/v1/accounts/lookup?acct={account}",
        "uri_pretty" : "https://expressional.social/@{account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_code" : 404,
        "m_string" : "Record not found",
        "known" : ["jippi", "poolesen"],
        "cat" : "social"
       },
       {
        "name" : "Eyeem",
        "uri_check" : "https://www.eyeem.com/u/{account}",
        "e_code" : 200,
        "e_string" : "Marketplace</title>",
        "m_string" : "Not Found (404) | EyeEm",
        "m_code" : 301,
        "known" : ["john", "bob"],
        "cat" : "art"
       },
       {
        "name" : "F3",
        "uri_check" : "https://f3.cool/{account}",
        "e_code" : 200,
        "e_string" : "<title>@",
        "m_string" : "Page Not Found - F3",
        "m_code" : 404,
        "known" : ["nick", "john"],
        "cat" : "social"
       },
       {
        "name" : "Fabswingers",
        "uri_check" : "https://www.fabswingers.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "View Profile",
        "m_string" : "The user you tried to view doesn't seem to be on the site any more",
        "m_code" : 200,
        "known" : ["justusboth2013", "hellfireclub", "fabswingers.com"],
        "cat" : "dating"
       },
       {
        "name" : "FACEIT",
        "uri_check" : "https://www.faceit.com/api/users/v1/nicknames/{account}",
        "uri_pretty" : "https://www.faceit.com/en/players/{account}",
        "e_code" : 200,
        "e_string" : "\"result\":\"OK\"",
        "m_string" : "\"message\":\"user not found\"",
        "m_code" : 404,
        "known" : ["s1mple", "w0nderful"],
        "cat" : "gaming"
       },
       {
        "name" : "Facebook",
        "uri_check" : "https://www.facebook.com/{account}/",
        "e_code" : 200,
        "e_string" : "__isProfile",
        "m_string" : "<title>Facebook</title>",
        "m_code" : 200,
        "known" : ["john.miniolic", "adam"],
        "cat" : "social"
       },
       {
        "name" : "Faktopedia",
        "uri_check" : "https://faktopedia.pl/user/{account}",
        "e_code" : 200,
        "e_string" : "Zamieszcza fakty od:",
        "m_string" : "Nie znaleziono użytkownika o podanym loginie.",
        "m_code" : 200,
        "known" : ["janek", "ania"],
        "cat" : "images"
       },
       {
        "name" : "FanCentro",
        "uri_check" : "https://fancentro.com/api/profile.get?profileAlias={account}&limit=1",
        "uri_pretty" : "https://fancentro.com/{account}/",
        "e_code" : 200,
        "e_string" : "\"status\":true",
        "m_string" : "\"status\":false",
        "m_code" : 200,
        "known" : ["medroxy","miaaamador"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "Fandom",
        "uri_check" : "https://www.fandom.com/u/{account}",
        "e_code" : 200,
        "e_string" : "| Profile | Fandom",
        "m_string" : "Not Found",
        "m_code" : 404,
        "known" : ["EJacobs94", "Drew_Dietsch"],
        "cat" : "gaming"
       },
       {
        "name" : "fanpop",
        "uri_check" : "https://www.fanpop.com/fans/{account}",
        "e_code" : 200,
        "e_string" : "Fanpopping since",
        "m_string" : "",
        "m_code" : 302,
        "known" : ["test", "johndoe"],
        "cat" : "social"
       },
       {
        "name" : "Fark",
        "uri_check" : "https://www.fark.com/users/{account}",
        "e_code" : 200,
        "e_string" : "Fark account number",
        "m_string" : "Tastes like chicken.",
        "m_code" : 200,
        "known" : ["bob", "bobby"],
        "cat" : "social"
       },
       {
        "name" : "fansly",
        "uri_check" : "https://apiv2.fansly.com/api/v1/account?usernames={account}",
        "uri_pretty" : "https://fansly.com/{account}/posts",
        "e_code" : 200,
        "e_string" : "username",
        "m_string" : "response: []",
        "m_code" : 200,
        "known" : ["Mikomin","test"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "FatSecret",
        "uri_check" : "https://www.fatsecret.com/member/{account}",
        "e_code" : 200,
        "e_string" : "- Member</title>",
        "m_string" : "Your Key to Success",
        "m_code" : 302,
        "known" : ["bob", "bobby"],
        "cat" : "health"
       },
       {
        "name" : "Federated.press (Mastodon Instance)",
        "uri_check" : "https://federated.press/api/v1/accounts/lookup?acct={account}",
        "uri_pretty" : "https://federated.press/@{account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_code" : 404,
        "m_string" : "Record not found",
        "known" : ["wood", "cliffcheney"],
        "cat" : "social"
       },
       {
        "name" : "figma",
        "uri_check" : "https://www.figma.com/@{account}",
        "e_code" : 200,
        "e_string" : ") on Figma Community",
        "m_string" : "The page you are looking for can't be found.",
        "m_code" : 404,
        "known" : ["bob", "mike"],
        "cat" : "tech"
       },
       {
        "name" : "Filmweb",
        "uri_check" : "https://www.filmweb.pl/user/{account}",
        "e_code" : 200,
        "e_string" : "profil w Filmweb</title>",
        "m_string" : "Varnish 404",
        "m_code" : 200,
        "known" : ["test", "Marcin_P"],
        "cat" : "hobby"
       },
       {
        "name" : "Filmot Channel Search",
        "uri_check" : "https://filmot.com/channelsearch/{account}",
        "e_code" : 200,
        "e_string" : "Subscribers",
        "m_string" : "No channels found",
        "m_code" : 200,
        "known" : ["bobicraft", "parodiadoranimado"],
        "cat" : "archived"
       },
       {
        "name" : "Filmot Unlisted Videos",
        "uri_check" : "https://filmot.com/unlistedSearch?channelQuery={account}&sortField=uploaddate&sortOrder=desc&",
        "e_code" : 200,
        "e_string" : "clips found",
        "m_string" : "No results",
        "m_code" : 200,
        "known" : ["holasoygerman", "elrubiusomg"],
        "cat" : "archived"
       },
       {
        "name" : "fine_art_america",
        "uri_check" : "https://fineartamerica.com/profiles/{account}",
        "e_code" : 200,
        "e_string" : "Shop for artwork by",
        "m_string" : "Browse through millions of independent artists in our extensive",
        "m_code" : 301,
        "known" : ["scott-norris", "mary-helmreich"],
        "cat" : "shopping"
       },
       {
        "name" : "Fiverr",
        "uri_check" : "https://www.fiverr.com/{account}",
        "e_code" : 200,
        "e_string" : "member-since",
        "m_string" : "",
        "m_code" : 302,
        "known" : ["yellowdd", "samanvay"],
        "cat" : "shopping"
       },
       {
        "name" : "Flickr",
        "uri_check" : "https://www.flickr.com/photos/{account}/",
        "e_code" : 200,
        "e_string" : "| Flickr",
        "m_string" : "",
        "m_code" : 404,
        "known" : ["glaciernps", "test"],
        "cat" : "images"
       },
       {
        "name" : "Flipboard",
        "uri_check" : "https://flipboard.com/@{account}",
        "e_code" : 200,
        "e_string" : ") on Flipboard",
        "m_string" : "<title></title>",
        "m_code" : 404,
        "known" : ["cosmopolitan", "Mashable"],
        "cat" : "tech"
       },
       {
        "name" : "flowcode",
        "uri_check" : "https://www.flowcode.com/page/{account}",
        "e_code" : 200,
        "e_string" : ";s Flowpage",
        "m_string" : "Nobody's reserved this Flowpage yet.",
        "m_code" : 404,
        "known" : ["evdokia", "irina"],
        "cat" : "social"
       },
       {
        "name" : "Folkd",
        "uri_check" : "https://www.folkd.com/?app=core&module=system&controller=ajax&do=usernameExists&input={account}",
        "uri_pretty" : "https://www.folkd.com/search/?q={account}&quick=1&type=core_members",
        "e_code" : 200,
        "e_string" : "\"message\":\"That display name is in use by another member.\"",
        "m_string" : "\"result\":\"ok\"",
        "m_code" : 200,
        "known" : ["smartplayapk", "abdulmerfantz"],
        "cat" : "social",
        "protection" : ["other"]
       },
       {
        "name" : "Fodors Forum",
        "uri_check" : "https://www.fodors.com/community/profile/{account}/forum-activity",
        "e_code" : 200,
        "e_string" : "User Profile | Fodor’s Travel</title>",
        "m_string" : "Plan Your Trip Online</title>",
        "m_code" : 302,
        "known" : ["jdstraveler", "gooster"],
        "cat" : "social"
       },
       {
        "name" : "Fortnite Tracker",
        "uri_check" : "https://fortnitetracker.com/profile/all/{account}",
        "e_code" : 200,
        "e_string" : "s Fortnite Stats - Fortnite Tracker",
        "m_string" : "Fortnite Player Stats -",
        "m_code" : 404,
        "known" : ["steph", "sam"],
        "cat" : "gaming"
       },
       {
        "name" : "forumprawne.org",
        "uri_check" : "https://forumprawne.org/members/{account}.html",
        "e_code" : 200,
        "e_string" : "Wiadomość",
        "m_string" : "",
        "m_code" : 500,
        "known" : ["test", "test2"],
        "cat" : "misc"
       },
       {
        "name" : "Fosstodon.org (Mastodon Instance)",
        "uri_check" : "https://fosstodon.org/api/v1/accounts/lookup?acct={account}",
        "uri_pretty" : "https://fosstodon.org/@{account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_code" : 404,
        "m_string" : "Record not found",
        "known" : ["linux", "Phil35"],
        "cat" : "social"
       },
       {
        "name" : "fotka",
        "uri_check" : "https://api.fotka.com/v2/user/dataStatic?login={account}",
        "uri_pretty" : "https://fotka.com/profil/{account}",
        "e_code" : 200,
        "e_string" : "profil",
        "m_string" : "ERROR",
        "m_code" : 200,
        "known" : ["test", "test2"],
        "cat" : "social"
       },
       {
        "name" : "Fotolog Archived Profile",
        "uri_check" : "https://archive.org/wayback/available?url=https://www.fotolog.com/{account}",
        "uri_pretty" : "https://web.archive.org/web/2/fotolog.com/{account}",
        "e_code" : 200,
        "e_string" : "\"archived_snapshots\": {\"closest\"",
        "m_string" : "\"archived_snapshots\": {}",
        "m_code" : 200,
        "known" : ["x_zudex_x", "angelito"],
        "cat" : "archived"
       },
       {
       "name" : "Foursquare",
        "uri_check" : "https://foursquare.com/{account}",
        "e_code" : 200,
        "e_string" : "on Foursquare</title>",
        "m_string" : "302 Found</title>",
        "m_code" : 302,
        "known" : ["john", "ncyp23"],
        "cat" : "social"
       },
       {
        "name" : "Freelancehunt Freelancer",
        "uri_check" : "https://freelancehunt.com/en/freelancer/{account}.html",
        "e_code" : 200,
        "e_string" : "\"@id\":\"https://freelancehunt.com/en/freelancers\"",
        "m_string" : "User not found.",
        "m_code" : 404,
        "known" : ["rhythmdev_top", "Zainka"],
        "cat" : "social",
        "protection" : ["other"]
       },
       {
        "name" : "Freelancehunt Employer",
        "uri_check" : "https://freelancehunt.com/en/employer/{account}.html",
        "e_code" : 200,
        "e_string" : "\"@id\":\"https://freelancehunt.com/en/employers\"",
        "m_string" : "User not found.",
        "m_code" : 404,
        "known" : ["vadym1232", "Dekovital"],
        "cat" : "social",
        "protection" : ["other"]
       },
       {
        "name" : "Freelance.ua",
        "uri_check" : "https://freelance.ua/user/{account}/",
        "e_code" : 200,
        "e_string" : "p-profile-avatar",
        "m_string" : "Схоже, дана сторінка не знайдена",
        "m_code" : 404,
        "known" : ["tkachenkoalex", "oleksandrseo1"],
        "cat" : "social"
       },
       {
        "name" : "FreeSteamKeys",
        "uri_check" : "https://www.freesteamkeys.com/members/{account}/",
        "e_code" : 200,
        "e_string" : "item-header-avatar",
        "m_string" : "error404",
        "m_code" : 404,
        "known" : ["giveaway-su", "keygenerator"],
        "cat" : "gaming"
       },
       {
        "name" : "Freelancer",
        "uri_check" : "https://www.freelancer.com/api/users/0.1/users?usernames%5B%5D={account}&compact=true",
        "uri_pretty" : "https://www.freelancer.com/u/{account}",
        "e_code" : 200,
        "e_string" : "\"users\":{\"",
        "m_string" : "\"users\":{}",
        "m_code" : 200,
        "known" : ["desiaunty", "creatvmind"],
        "cat" : "business"
       },
       {
        "name" : "freesound",
        "uri_check" : "https://freesound.org/people/{account}/",
        "e_code" : 200,
        "e_string" : "Has been a user for",
        "m_string" : "Page not found</title>",
        "m_code" : 404,
        "known" : ["test", "JohnDoe"],
        "cat" : "music"
       },
       {
        "name" : "FriendFinder",
        "uri_check" : "https://friendfinder.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "Last Visit:",
        "m_string" : "302 Found",
        "m_code" : 302,
        "known" : ["alex56", "john"],
        "cat" : "dating"
       },
       {
        "name" : "FriendFinder-X",
        "uri_check" : "https://www.friendfinder-x.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "'s Dating Profile on FriendFinder-x",
        "m_string" : "The document has moved",
        "m_code" : 302,
        "known" : ["john"],
        "cat" : "dating"
       },
       {
        "name" : "FurAffinity",
        "uri_check" : "https://www.furaffinity.net/user/{account}",
        "e_code" : 200,
        "e_string" : "<title>Userpage of",
        "m_string" : "user cannot be found",
        "m_code" : 200,
        "known" : ["karintina", "mikrogoat"],
        "cat" : "images"
       },
       {
        "name" : "Gab",
        "uri_check" : "https://gab.com/api/v1/account_by_username/{account}",
        "uri_pretty" : "https://gab.com/{account}",
        "e_code" : 200,
        "e_string" : "followers_count",
        "m_string" : "Record not found",
        "m_code" : 404,
        "known" : ["RealMarjorieGreene", "LaurenBoebert"],
        "cat" : "political"
       },
       {
        "name" : "game_debate",
        "uri_check" : "https://www.game-debate.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "| , , GB pc game performance",
        "m_string" : "Not Found",
        "m_code" : 404,
        "known" : ["Johnboy", "Crazy"],
        "cat" : "gaming"
       },
       {
        "name" : "Game Jolt",
        "uri_check" : "https://gamejolt.com/site-api/web/profile/@{account}/",
        "uri_pretty" : "https://gamejolt.com/@{account}",
        "e_code" : 200,
        "e_string" : "created_on",
        "m_string" : "null,",
        "m_code" : 404,
        "known" : ["nilllzz", "KorbloxTeams"],
        "cat" : "gaming"
       },
       {
        "name" : "Gamespot",
        "uri_check" : "https://www.gamespot.com/profile/{account}/",
        "e_code" : 200,
        "e_string" : "'s Profile - GameSpot</title>",
        "m_string" : "404: Not Found - GameSpot</title>",
        "m_code" : 200,
        "known" : ["alice", "bob"],
        "cat" : "gaming"
       },
       {
        "name" : "Garmin connect",
        "uri_check" : "https://connect.garmin.com/modern/profile/{account}",
        "e_code" : 200,
        "e_string" : "window.ERROR_VIEW = null",
        "m_string" : "resourceNotFoundRoute",
        "m_code" : 200,
        "known" : ["tommy", "cderalow"],
        "cat" : "health"
       },
       {
         "name" : "GDBrowser",
         "uri_check" : "https://gdbrowser.com/u/{account}",
         "e_code" : 200,
         "e_string" : "<div class=\"popup\" id=\"statsDiv\"",
         "m_string" : "<p>Found. Redirecting to ",
         "m_code" : 302,
         "known" : ["SorkoPiko", "Subwoofer"],
         "cat" : "gaming"
       },
       {
        "name" : "GeeksForGeeks",
        "uri_check" : "https://authapi.geeksforgeeks.org/api-get/user-profile-info/?handle={account}",
        "uri_pretty" : "https://www.geeksforgeeks.org/user/{account}/",
        "e_code" : 200,
        "e_string" : "\"message\":\"data retrieved successfully\"",
        "m_code" : 400,
        "m_string" : "\"message\":\"User not found!\"",
        "known" : ["nath_789", "harshrajsinghsiwan", "igovindindia"],
        "cat" : "coding"
       },
       {
        "name" : "Geocaching",
        "uri_check" : "https://www.geocaching.com/p/?u={account}",
        "e_code" : 200,
        "e_string" : "Groundspeak - User Profile",
        "m_string" : "Error 404: DNF",
        "m_code" : 404,
        "known" : ["moun10bike", "niraD"],
        "cat" : "social"
       },
       {
        "name" : "getmonero",
        "uri_check" : "https://forum.getmonero.org/user/{account}",
        "e_code" : 200,
        "e_string" :"Monero | User",
        "m_string" : "Monero | Page not found. Error: 404",
        "m_code" : 200,
        "known" : ["silverfox", "monero"],
        "cat" : "misc"
       },
       {
        "name" : "Gettr",
        "uri_check" : "https://api.gettr.com/s/user/{account}/exist",
        "uri_pretty" : "https://gettr.com/user/{account}",
        "e_code" : 200,
        "e_string" : "success\":{",
        "m_string" : "success\":false",
        "m_code" : 200,
        "known" : ["gettr", "support"],
        "cat" : "social"
       },
       {
        "name" : "Gigapan",
        "uri_check" : "https://www.gigapan.com/profiles/{account}",
        "e_code" : 200,
        "e_string" : "width=\"100\"",
        "m_string" : "<a href=\"/gigapans\">View Gigapans</a>",
        "m_code" : 404,
        "known" : ["test", "lucahammer"],
        "cat" : "hobby"
       },
       {
        "name" : "Giphy (Channel)",
        "uri_check" : "https://giphy.com/channel/{account}",
        "e_code" : 200,
        "e_string" : "\\\"user_id\\\"",
        "m_string" : "404 Not Found",
        "m_code" : 404,
        "known" : ["teddy_99", "LastYear"],
        "cat" : "images",
        "protection" : ["other"]
       },
       {
        "name" : "Gitea",
        "uri_check" : "https://gitea.com/{account}",
        "e_code" : 200,
        "e_string" : "class=\"page-content user profile\"",
        "m_string" : "class=\"status-page-error\"",
        "m_code" : 404,
        "known" : ["xin", "dev"],
        "cat" : "coding"
       },
       {
        "name" : "giters",
        "uri_check" : "https://giters.com/{account}",
        "e_code" : 200,
        "e_string" : " - Giters</title>",
        "m_string" : "This page could not be found</title>",
        "m_code" : 404,
        "known" : ["WebBreacher", "C3n7ral051nt4g3ncy"],
        "cat" : "coding"
       },
       {
        "name" : "GitHub",
        "uri_check" : "https://github.com/{account}",
        "e_code" : 200,
        "e_string" : "p-nickname vcard-username d-block",
        "m_string" : "Not Found",
        "m_code" : 404,
        "known" : ["test", "WebBreacher"],
        "cat" : "coding",
        "headers" : {
            "accept" : "text/html"
        }
       },
       {
        "name" : "GitLab",
        "uri_check" : "https://gitlab.com/users/{account}/exists",
        "uri_pretty" : "https://gitlab.com/{account}",
        "e_code" : 200,
        "e_string" : "\"exists\":true",
        "m_string" : "\"exists\":false",
        "m_code" : 200,
        "known" : ["skennedy", "KennBro"],
        "cat" : "coding"
       },
       {
        "name" : "Gitee",
        "uri_check" : "https://gitee.com/{account}",
        "e_code" : 200,
        "e_string" : "class=\"ui container user_page\"",
        "m_string" : "class=\"container error midCenter\"",
        "m_code" : 404,
        "known" : ["maxim", "fupengfei"],
        "cat" : "coding"
       },
       {
        "name" : "gloria.tv",
        "uri_check" : "https://gloria.tv/{account}",
        "e_code" : 200,
        "e_string" : "Last online",
        "m_string" : "Page unavailable",
        "m_code" : 404,
        "known" : ["Irapuato", "en.news"],
        "cat" : "social"
       },
       {
        "name" : "GNOME GitLab",
        "uri_check" : "https://gitlab.gnome.org/{account}",
        "e_code" : 200,
        "e_string" : "class=\"user-profile-content\"",
        "m_string" : ">redirected</a>",
        "m_code" : 302,
        "known" : ["MystikNinja", "0xMRTT"],
        "cat" : "coding"
       },
       {
        "name" : "GNOME Shell Extensions",
        "uri_check" : "https://extensions.gnome.org/accounts/profile/{account}",
        "e_code" : 200,
        "e_string" : "class=\"user-details\"",
        "m_string" : "<h3>404 - Page not Found</h3>",
        "m_code" : 404,
        "known" : ["johnny", "dev"],
        "cat" : "coding"
       },
       {
        "name" : "GOG",
        "uri_check" : "https://www.gog.com/u/{account}",
        "e_code" : 200,
        "e_string" : "window.profilesData.profileUser",
        "m_code" : 302,
        "m_string" : "href=\"http://www.gog.com/404\"",
        "known" : ["user", "Admin"],
        "cat" : "gaming"
       },
       {
        "name" : "Goodgame_Russia",
        "uri_check" : "https://goodgame.ru/channel/{account}/",
        "e_code" : 200,
        "e_string" : "channel_id",
        "m_string" : "Такой страницы не существует",
        "m_code" : 400,
        "known" : ["ejysarmat", "JacksonTV"],
        "cat" : "gaming"
       },
       {
        "name" : "gpodder.net",
        "uri_check" : "https://gpodder.net/user/{account}/",
        "e_code" : 200,
        "e_string" : "mdash; gpodder.net",
        "m_string" : "404 - Not found",
        "m_code" : 404,
        "known" : ["blue", "red"],
        "cat" : "music"
       },
       {
        "name" : "grandprof",
        "uri_check" : "https://grandprof.org/communaute/{account}",
        "e_code" : 200,
        "e_string" : "s Profile",
        "m_string" : "Mauvaise pioche",
        "m_code" : 404,
        "known" : ["mohamed01", "amine"],
        "cat" : "misc"
       },
       {
        "name" : "Gravatar",
        "uri_check" : "https://en.gravatar.com/{account}.json",
        "uri_pretty" : "https://en.gravatar.com/{account}",
        "e_code" : 200,
        "e_string" : "entry",
        "m_string" : "User not found",
        "m_code" : 404,
        "known" : ["test"],
        "cat" : "images"
       },
       {
        "name" : "Graphics.social (Mastodon Instance)",
        "uri_check" : "https://graphics.social/api/v1/accounts/lookup?acct={account}",
        "uri_pretty" : "https://graphics.social/@{account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_code" : 404,
        "m_string" : "Record not found",
        "known" : ["brian", "moonpotato"],
        "cat" : "social"
       },
       {
        "name" : "GTAinside.com",
        "uri_check" : "https://www.gtainside.com/user/{account}",
        "e_code" : 200,
        "e_string" : "userpage_user",
        "m_string" : "<h1>404 Not Found",
        "m_code" : 200,
        "known" : ["daniel", "franco"],
        "cat" : "gaming"
       },
       {
        "name" : "gumroad",
        "uri_check" : "https://{account}.gumroad.com/",
        "strip_bad_char" : ".",
        "e_code" : 200,
        "e_string" : "s profile picture",
        "m_string" : "Page not found",
        "m_code" : 404,
        "known" : ["ellietalksmoney", "reallyniceimages"],
        "cat" : "shopping"
       },
       {
        "name" : "Habr",
        "uri_check" : "https://habr.com/ru/users/{account}/",
        "e_code" : 200,
        "e_string" : "tm-page tm-user",
        "m_string" : "tm-error-message",
        "m_code" : 404,
        "known" : ["Bo0oM", "AlhimicMan"],
        "cat" : "social"
       },
       {
        "name" : "Habr Freelancer",
        "uri_check" : "https://freelance.habr.com/freelancers/{account}",
        "e_code" : 200,
        "e_string" : "user-profile profile-blocks",
        "m_string" : "icon_user_locked",
        "m_code" : 404,
        "known" : ["Bo0oM", "Akloom"],
        "cat" : "social"
       },
       {
        "name" : "Habr Employer",
        "uri_check" : "https://freelance.habr.com/freelancers/{account}/employer",
        "e_code" : 200,
        "e_string" : "user-profile profile-blocks",
        "m_string" : "icon_user_locked",
        "m_code" : 404,
        "known" : ["aufdk", "Danvantariy"],
        "cat" : "social"
       },
       {
        "name" : "Habr Q&A",
        "uri_check" : "https://qna.habr.com/user/{account}",
        "e_code" : 200,
        "e_string" : "class=\"page-header__info\"",
        "m_string" : "icon_error_404",
        "m_code" : 404,
        "known" : ["Masthead", "dmitriypur"],
        "cat" : "coding"
       },
       {
        "name" : "Habbo.com",
        "uri_check" : " https://www.habbo.com/api/public/users?name={account}",
        "uri_pretty" : " https://www.habbo.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "currentLevel",
        "m_string" : "not-found",
        "m_code" : 404,
        "known" : ["john", "michelle"],
        "cat" : "gaming"
       },
       {
        "name" : "Habbo.es",
        "uri_check" : " https://www.habbo.es/api/public/users?name={account}",
        "uri_pretty" : " https://www.habbo.es/profile/{account}",
        "e_code" : 200,
        "e_string" : "currentLevel",
        "m_string" : "not-found",
        "m_code" : 404,
        "known" : ["juan", "michelle"],
        "cat" : "gaming"
       },
       {
        "name" : "Habbo.com.br",
        "uri_check" : "https://www.habbo.com.br/api/public/users?name={account}",
        "uri_pretty" : "https://www.habbo.com.br/profile/{account}",
        "e_code" : 200,
        "e_string" : "currentLevel",
        "m_string" : "not-found",
        "m_code" : 404,
        "known" : ["jeaniucas", "cellao"],
        "cat" : "gaming"
       },
       {
        "name" : "Habbo.de",
        "uri_check" : "https://www.habbo.de/api/public/users?name={account}",
        "uri_pretty" : "https://www.habbo.de/profile/{account}",
        "e_code" : 200,
        "e_string" : "currentLevel",
        "m_string" : "not-found",
        "m_code" : 404,
        "known" : ["klaus", "angelinaa"],
        "cat" : "gaming"
       },
       {
        "name" : "Habbo.com.tr",
        "uri_check" : "https://www.habbo.com.tr/api/public/users?name={account}",
        "uri_pretty" : "https://www.habbo.com.tr/profile/{account}",
        "e_code" : 200,
        "e_string" : "currentLevel",
        "m_string" : "not-found",
        "m_code" : 404,
        "known" : ["fatma9180", "elektrikci"],
        "cat" : "gaming"
       },
       {
        "name" : "Habbo.fr",
        "uri_check" : "https://www.habbo.fr/api/public/users?name={account}",
        "uri_pretty" : "https://www.habbo.fr/profile/{account}",
        "e_code" : 200,
        "e_string" : "currentLevel",
        "m_string" : "not-found",
        "m_code" : 404,
        "known" : ["2006", "sicilienne"],
        "cat" : "gaming"
       },
       {
        "name" : "Habbo.it",
        "uri_check" : "https://www.habbo.it/api/public/users?name={account}",
        "uri_pretty" : "https://www.habbo.it/profile/{account}",
        "e_code" : 200,
        "e_string" : "currentLevel",
        "m_string" : "not-found",
        "m_code" : 404,
        "known" : ["samsebek", "papablu"],
        "cat" : "gaming"
       },
       {
        "name" : "Habbo.nl",
        "uri_check" : "https://www.habbo.nl/api/public/users?name={account}",
        "uri_pretty" : "https://www.habbo.nl/profile/{account}",
        "e_code" : 200,
        "e_string" : "currentLevel",
        "m_string" : "not-found",
        "m_code" : 404,
        "known" : ["XOTWOD.xx", "xoSorxo"],
        "cat" : "gaming"
       },
       {
        "name" : "Habbo.fi",
        "uri_check" : "https://www.habbo.fi/api/public/users?name={account}",
        "uri_pretty" : "https://www.habbo.fi/profile/{account}",
        "e_code" : 200,
        "e_string" : "currentLevel",
        "m_string" : "not-found",
        "m_code" : 404,
        "known" : ["cucumberz", "Yasline"],
        "cat" : "gaming"
       },
       {
        "name" : "Habtium",
        "uri_check" : "https://habtium.es/{account}",
        "e_code" : 200,
        "e_string" : "<div class=\"profile-info",
        "m_string" : "<h1 class=\"section red\">Oops!",
        "m_code" : 404,
        "known" : ["diegjeremy", "suigetsu"],
        "cat" : "gaming"
       },
       {
        "name" : "Hackaday",
        "uri_check" : "https://hackaday.io/{account}",
        "e_code" : 200,
        "e_string" : "'s Profile | Hackaday.io",
        "m_string" : "The requested URL was not found on this server. That’s all we know.",
        "m_code" : 404,
        "known" : ["john", "adam"],
        "cat" : "hobby"
       },
       {
        "name" : "hackrocks",
        "uri_check" : "https://hackrocks.com/api/users/profile",
        "uri_pretty" : "https://hackrocks.com/id/{account}",
        "post_body" : "{\"username\":\"{account}\"}",
        "e_code" : 200,
        "e_string" : "\"username\":",
        "m_string" : "\"error_data\":\"USER_NOT_FOUND\"",
        "m_code" : 404,
        "known" : ["mespejo", "NeoWaveCode"],
        "cat" : "tech",
        "headers" : {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json"
        }
       },
       {
        "name" : "Hacker News",
        "uri_check" : "https://news.ycombinator.com/user?id={account}",
        "e_code" : 200,
        "e_string" : "created:",
        "m_string" : "No such user.",
        "m_code" : 200,
        "known" : ["mubix", "egypt"],
        "cat" : "tech"
       },
       {
        "name" : "Hackernoon",
        "uri_check" : "https://hackernoon.com/_next/data/foL6JC7ro2FEEMD-gMKgQ/u/{account}.json",
        "uri_pretty" : "https://hackernoon.com/u/{account}",
        "e_code" : 200,
        "e_string" : "\"profile\"",
        "m_string" : "__N_REDIRECT",
        "m_code" : 200,
        "known" : ["john", "alex"],
        "cat" : "tech"
       },
       {
        "name" : "hackerearth",
        "uri_check" : "https://www.hackerearth.com/@{account}",
        "e_code" : 200,
        "e_string" : "| Developer Profile on HackerEarth",
        "m_string" : "404 | HackerEarth",
        "m_code" : 200,
        "known" : ["peter", "liam"],
        "cat" : "coding"
       },
       {
        "name" : "HackerOne",
        "uri_check" : "https://hackerone.com/graphql",
        "uri_pretty" : "https://hackerone.com/{account}",
        "post_body" : "{\"query\":\"query($url: URI!) {\\n        resource(url: $url) {\\n            ... on User { username }\\n        }\\n    }\",\"variables\":{\"url\":\"{account}\"}}",
        "e_code" : 200,
        "e_string" : "\"username\":",
        "m_string" : "\"type\":\"NOT_FOUND\"",
        "m_code" : 200,
        "known" : ["born2hack", "godiego"],
        "cat" : "tech",
        "headers" : {
            "Content-Type": "application/json"
        }
       },
       {
        "name" : "HackerRank",
        "uri_check" : "https://www.hackerrank.com/rest/contests/master/hackers/{account}/profile",
        "uri_pretty" : "https://www.hackerrank.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "\"model\":",
        "m_string" : "\"error\":\"Not Found\"",
        "m_code" : 404,
        "known" : ["FMota", "adepanges"],
        "cat" : "tech",
        "protection" : ["other"]
       },
       {
        "name" : "Hackster",
        "uri_check" : "https://www.hackster.io/{account}",
        "e_code" : 200,
        "e_string" : "data-hypernova-key=\"UserProfile\"",
        "m_string" : "id=\"error\"",
        "m_code" : 404,
        "known" : ["hendra", "sologithu"],
        "cat" : "coding"
       },
       {
        "name" : "hamaha",
        "uri_check" : "https://hamaha.net/{account}",
        "e_code" : 200,
        "e_string" : "- трейдинг форекс фьючерсы акции фондовый рынок ",
        "m_string" : "HAMAHA  Биткоин форум.",
        "m_code" : 200,
        "known" : ["oleg", "misha"],
        "cat" : "finance"
       },
       {
        "name" : "Hanime",
        "uri_check" : "https://hanime.tv/channels/{account}",
        "e_code" : 200,
        "e_string" : "Channel Views",
        "m_code" : 302,
        "m_string" : "DYNAMIC",
        "known" : ["thecolorred-7902", "arisu-cum-stats-2787"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "Hcommons.social (Mastodon Instance)",
        "uri_check" : "https://hcommons.social/api/v1/accounts/lookup?acct={account}",
        "uri_pretty" : "https://hcommons.social/@{account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_code" : 404,
        "m_string" : "Record not found",
        "known" : ["hello", "iuulaio"],
        "cat" : "social"
       },
       {
        "name" : "Heylink",
        "uri_check" : "https://heylink.me/{account}/",
        "e_code" : 200,
        "e_string" : "HeyLink.me |",
        "m_string" : "We can't find the page that you're looking for :(",
        "m_code" : 404,
        "known" : ["mohammed13", "johnny"],
        "cat" : "misc"
       },
       {
        "name" : "hiberworld",
        "uri_check" : "https://hiberworld.com/user/{account}",
        "e_code" : 200,
        "e_string" : "Member since ",
        "m_string" : "Looks like you got lost ",
        "m_code" : 200,
        "known" : ["Axeman", "Silver01"],
        "cat" : "gaming"
       },
       {
        "name" : "HiHello",
        "uri_check" : "https://www.hihello.me/author/{account}",
        "e_code" : 200,
        "e_string" : "<title>HiHello Blog Author: ",
        "m_string" : "Well, this is awkward",
        "m_code" : 404,
        "known" : ["pascal-theriault", "kortnee-paiha"],
        "cat" : "business"
       },
       {
        "name" : "Historians.social (Mastodon Instance)",
        "uri_check" : "https://historians.social/api/v1/accounts/lookup?acct={account}",
        "uri_pretty" : "https://historians.social/@{account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_code" : 404,
        "m_string" : "Record not found",
        "known" : ["lizcovart", "Ejoiner"],
        "cat" : "social"
       },
       {
        "name" : "HomeDesign3D",
        "uri_check" : "https://en.homedesign3d.net/user/{account}",
        "e_code" : 200,
        "e_string" : "userspace",
        "m_string" : "An Error Occurred: Internal Server Error",
        "m_code" : 500,
        "known" : ["carlos01", "paul"],
        "cat" : "hobby"
       },
       {
        "name" : "Holopin",
        "uri_check" : "https://holopin.io/@{account}#",
        "e_code" : 200,
        "e_string" : " | Holopin</title>",
        "m_code" : 200,
        "m_string" : "Not found</div>",
        "known" : ["holo", "test"],
        "cat" : "hobby"
       },
       {
        "name" : "Hometech.social (Mastodon Instance)",
        "uri_check" : "https://hometech.social/api/v1/accounts/lookup?acct={account}",
        "uri_pretty" : "https://hometech.social/@{account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_code" : 404,
        "m_string" : "Record not found",
        "known" : ["one4ll", "seth"],
        "cat" : "social"
       },
       {
        "name" : "hoo.be",
        "uri_check" : "https://hoo.be/{account}",
        "e_code" : 200,
        "e_string" : "--profile-name-color",
        "m_string" : "Page Not Found</h3>",
        "m_code" : 404,
        "known" : ["chrishemsworth", "alextackie"],
        "cat" : "business"
       },
       {
        "name" : "Hostux.social (Mastodon Instance)",
        "uri_check" : "https://hostux.social/api/v1/accounts/lookup?acct={account}",
        "uri_pretty" : "https://hostux.social/@{account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_code" : 404,
        "m_string" : "Record not found",
        "known" : ["alarig", "rsmela"],
        "cat" : "social"
       },
       {
        "name" : "Houzz",
        "uri_check" : "https://www.houzz.com/user/{account}",
        "e_code" : 200,
        "e_string" : "Followers",
        "m_string" : "Page Not Found",
        "m_code" : 404,
        "known" : ["liam", "alex"],
        "cat" : "hobby"
       },
       {
        "name" : "HubPages",
        "uri_check" : "https://hubpages.com/@{account}",
        "e_code" : 200,
        "e_string" : "name\">Followers",
        "m_string" : "Sorry, that user does not exist",
        "m_code" : 404,
        "known" : ["greeneyes1607", "lmmartin"],
        "cat" : "blog"
       },
       {
        "name" : "Hubski",
        "uri_check" : "https://hubski.com/user/{account}",
        "e_code" : 200,
        "e_string" : "'s profile",
        "m_string" : "No such user.",
        "m_code" : 200,
        "known" : ["john", "blue"],
        "cat" : "social"
       },
       {
        "name" : "HudsonRock",
        "uri_check" : "https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-username?username={account}",
        "e_code" : 200,
        "e_string" : "This username is associated with a computer that was infected by an info-stealer",
        "m_string" : "This username is not associated with a computer infected by an info-stealer",
        "m_code" : 200,
        "known" : ["testadmin", "testadmin1"],
        "cat" : "tech"
       },
       {
        "name" : "hugging_face",
        "uri_check" : "https://huggingface.co/{account}",
        "e_code" : 200,
        "e_string" : "thumbnails.huggingface.co/social-thumbnails/",
        "m_string" : "Sorry, we can't find the page you are looking for.",
        "m_code" : 404,
        "known" : ["hack", "dev"],
        "cat" : "tech"
       },
       {
        "name" : "Iconfinder",
        "uri_check" : "https://www.iconfinder.com/{account}",
        "e_code" : 200,
        "e_string" : "data-to-user-id=",
        "m_string" : "We couldn't find the page you are looking for.",
        "m_code" : 404,
        "known" : ["roundicons", "iconfinder"],
        "cat" : "images"
       },
       {
        "name" : "icq-chat",
        "uri_check" : "https://icq.icqchat.co/members/{account}/",
        "e_code" : 200,
        "e_string" : "Last seen",
        "m_string" : "Oops! We ran into some problems",
        "m_code" : 404,
        "known" : ["brookenora.54", "bigdaddy.77"],
        "cat" : "social"
       },
       {
        "name" : "IFTTT",
        "uri_check" : "https://ifttt.com/p/{account}",
        "e_code" : 200,
        "e_string" : "Joined",
        "m_string" : "The requested page or file does not exist",
        "m_code" : 404,
        "known" : ["nr9992", "sss90"],
        "cat" : "misc"
       },
       {
        "name" : "ifunny",
        "uri_check" : "https://ifunny.co/user/{account}",
        "e_code" : 200,
        "e_string" :"subscribers",
        "m_string" : "404 - page not found",
        "m_code" : 404,
        "known" : ["hacker", "john"],
        "cat" : "misc"
       },
       {
        "name" : "igromania",
        "uri_check" : "http://forum.igromania.ru/member.php?username={account}",
        "e_code" : 200,
        "e_string" : "Форум Игромании - Просмотр профиля:",
        "m_string" : "Пользователь не зарегистрирован и не имеет профиля для просмотра.",
        "m_code" : 200,
        "known" : ["bob", "blue"],
        "cat" : "social"
       },
       {
        "name" : "ilovegrowingmarijuana",
        "uri_check" : "https://support.ilovegrowingmarijuana.com/u/{account}",
        "e_code" : 200,
        "e_string" : "<title>  Profile - ",
        "m_string" : "Oops! That page doesn’t exist or is private",
        "m_code" : 404,
        "known" : ["ILGM.Stacy", "Mosaicmind9x"],
        "cat" : "social"
       },
       {
        "name" : "imagefap",
        "uri_check" : "https://www.imagefap.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "s Profile",
        "m_string" : "Invalid uid",
        "m_code" : 200,
        "known" : ["lover03", "SecretSide15"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "ImageShack",
        "uri_check" : "https://imageshack.com/user/{account}",
        "e_code" : 200,
        "e_string" : "s Images</title>",
        "m_string" : "",
        "m_code" : 302,
        "known" : ["test"],
        "cat" : "images"
       },
       {
        "name" : "iMGSRC.RU",
        "uri_check" : "https://imgsrc.ru/main/user.php?lang=ru&user={account}",
        "e_code" : 200,
        "e_string" : "Присоединился",
        "m_string" : "",
        "m_code" : 302,
        "known" : ["natalisn","andydiamond","natalyck"],
        "cat" : "images"
       },
       {
        "name" : "imgur",
        "uri_check" : "https://api.imgur.com/account/v1/accounts/{account}?client_id=546c25a59c58ad7&include=trophies%2Cmedallions",
        "uri_pretty" : "https://imgur.com/user/{account}/about",
        "e_code" : 200,
        "e_string" : "created_at",
        "m_string" : "unable to find account",
        "m_code" : 404,
        "known" : ["OliverClothesoff70", "DadOnTheInternet"],
        "cat" : "images"
       },
       {
        "name" : "inaturalist",
        "uri_check" : "https://inaturalist.nz/people/{account}",
        "e_code" : 200,
        "e_string" : "s Profile",
        "m_string" : "404 Not Found",
        "m_code" : 404,
        "known" : ["greg", "tom"],
        "cat" : "hobby"
       },
       {
        "name" : "Independent academia",
        "uri_check" : "https://independent.academia.edu/{account}",
        "e_code" : 200,
        "e_string" : "- Academia.edu",
        "m_string" : "Academia.edu",
        "m_code" : 404,
        "known" : ["peter", "LiamM"],
        "cat" : "hobby"
       },
       {
        "name" : "InkBunny",
        "uri_check" : "https://inkbunny.net/{account}",
        "e_code" : 200,
        "e_string" : "Profile | Inkbunny, the Furry Art Community</title>",
        "m_string" : "<title>Members | Inkbunny, the Furry Art Community</title>",
        "m_code" : 302,
        "known" : ["AdminBunny", "test"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "InsaneJournal",
        "uri_check" : "https://{account}.insanejournal.com/profile",
        "strip_bad_char" : ".",
        "e_code" : 200,
        "e_string" : "User:",
        "m_string" : "The requested URL /profile was not found on this server",
        "m_code" : 200,
        "known" : ["test", "pint-sized", "acroamatica"],
        "cat" : "social"
       },
       {
        "name" : "Instagram",
        "uri_pretty" : "https://instagram.com/{account}",
        "uri_check" : "https://www.picuki.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "Instagram public profile with posts",
        "m_string" : "Nothing found!",
        "m_code" : 404,
        "known" : ["katyperry", "kirbstr"],
        "cat" : "social"
       },
       {
        "name" : "Instagram (Imginn)",
        "uri_check" : "https://imginn.com/{account}/",
        "e_code" : 200,
        "e_string" : "userinfo",
        "m_string" : "page-error notfound",
        "m_code" : 404,
        "known" : ["therock", "ramarim"],
        "cat" : "social",
        "protection" : ["cloudflare"]
       },
       {
        "name" : "Instagram2",
        "uri_pretty" : "https://instagram.com/{account}",
        "uri_check" : "https://dumpoir.com/v/{account}",
        "e_code" : 200,
        "e_string" : "Instagram Stories, Profile, Posts and Followers View Anonymous",
        "m_string" : "We are sorry. Should we search anything else?",
        "m_code" : 404,
        "known" : [
          "katyperry",
          "kirbstr"
        ],
        "cat" : "social"
       },
       {
        "name" : "Instagram_archives",
        "uri_check" : "https://archive.org/wayback/available?url=https://instagram.com/{account}/",
        "e_code" : 200,
        "e_string" : "\"archived_snapshots\": {\"closest\"",
        "m_string" : "\"archived_snapshots\": {}}",
        "m_code" : 200,
        "known" : ["zuck", "jack"],
        "cat" : "social"
       },
       {
        "name" : "Instructables",
        "uri_check" : "https://www.instructables.com/json-api/showAuthorExists?screenName={account}",
        "uri_pretty" : "https://www.instructables.com/member/{account}/",
        "e_code" : 200,
        "e_string" : "\"exists\": true",
        "m_string" : "\"error\": \"Sorry, we couldn't find that one!\"",
        "m_code" : 404,
        "known" : ["davidandora", "test"],
        "cat" : "hobby"
       },
       {
        "name" : "Internet Archive User Search",
        "uri_check" : "https://archive.org/advancedsearch.php?q={account}&output=json",
        "uri_pretty" : "https://archive.org/search.php?query={account}",
        "e_code" : 200,
        "e_string" : "backup_location",
        "m_string" : "numFound\":0",
        "m_code" : 200,
        "known" : ["test", "mubix"],
        "cat" : "misc"
       },
       {
        "name" : "interpals",
        "uri_check" : "https://www.interpals.net/{account}",
        "e_code" : 200,
        "e_string" : "Looking for",
        "m_string" : "User not found",
        "m_code" : 200,
        "known" : ["test"],
        "cat" : "dating"
       },
       {
        "name" : "Intigriti",
        "uri_check" : "https://app.intigriti.com/api/user/public/profile/{account}",
        "uri_pretty" : "https://app.intigriti.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "\"userName\":",
        "m_string" : "class=\"error-page-container\"",
        "m_code" : 404,
        "known" : ["vampire01", "kenshiin"],
        "cat" : "tech"
       },
       {
        "name" : "isMyGirl",
        "uri_check" : "https://api.fxcservices.com/pub/user/{account}",
        "uri_pretty" : "https://ismygirl.com/{account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_code" : 404,
        "m_string" : "User does not exist",
        "known" : ["kasumineechan", "blinky"],
        "cat" : "finance"
       },
       {
        "name" : "issuu",
        "uri_check" : "https://issuu.com/{account}",
        "e_code" : 200,
        "e_string" : "- Issuu",
        "m_string" : "Oops — we can’t seem to find the page you’re looking for.",
        "m_code" : 404,
        "known" : ["john", "smith"],
        "cat" : "shopping"
       },
       {
        "name" : "itch.io",
        "uri_check" : "https://itch.io/profile/{account}",
        "e_code" : 200,
        "e_string" : "A member registered",
        "m_code" : 404,
        "m_string" : "We couldn't find your page",
        "known" : ["prestent", "finch"],
        "cat" : "gaming"
       },
       {
        "name" : "Japandict",
        "uri_check" : "https://forum.japandict.com/u/{account}",
        "e_code" : 200,
        "e_string" : "modern browser",
        "m_code" : 404,
        "m_string" : "The page you requested could not be found.",
        "known" : ["Yan", "Happy"],
        "cat" : "social"
       },
       {
        "name" : "jeja.pl",
        "uri_check" : "https://www.jeja.pl/user,{account}",
        "e_code" : 200,
        "e_string" : "Profil użytkownika",
        "m_string" : "Niepoprawny login",
        "m_code" : 200,
        "known" : ["kowal", "janek"],
        "cat" : "misc"
       },
       {
        "name" : "JBZD",
        "uri_check" : "https://jbzd.com.pl/uzytkownik/{account}",
        "e_code" : 200,
        "e_string" : "Dzidy użytkownika",
        "m_string" : "Błąd 404",
        "m_code" : 404,
        "known" : ["test", "janek"],
        "cat" : "images"
       },
       {
        "name" : "Jeuxvideo",
        "uri_check" : "https://www.jeuxvideo.com/profil/{account}?mode=infos",
        "e_code" : 200,
        "e_string" : "- jeuxvideo.com",
        "m_string" : "rence des gamers",
        "m_code" : 404,
        "known" : ["jane", "alex"],
        "cat" : "gaming"
       },
       {
        "name" : "Joe Monster",
        "uri_check" : "https://joemonster.org/bojownik/{account}",
        "e_code" : 200,
        "e_string" : "jest prywatny",
        "m_string" : "Nie wiem jak ci to powiedzieć",
        "m_code" : 200,
        "known" : ["dandris", "lasior"],
        "cat" : "misc"
       },
       {
        "name" : "JSFiddle",
        "uri_check" : "https://jsfiddle.net/user/{account}/",
        "e_code" : 200,
        "e_string" : "Settings - JSFiddle - Code Playground",
        "m_string" : "That page doesn't exist.",
        "m_code" : 404,
        "known" : ["john", "alex"],
        "cat" : "coding"
       },
       {
        "name" : "Justforfans",
        "uri_check" : "https://justfor.fans/{account}",
        "e_code" : 200,
        "e_string" : " @ JustFor.Fans",
        "m_string" : "",
        "m_code" : 302,
        "known" : ["devinfrancoxxx", "RileyChaux"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "kaggle",
        "uri_check" : "https://www.kaggle.com/{account}",
        "e_code" : 200,
        "e_string" : "| Kaggle",
        "m_string" : "Kaggle: Your Home for Data Science",
        "m_code" : 404,
        "known" : ["babyoda", "residentmario"],
        "cat" : "coding"
       },
       {
        "name" : "Keybase",
        "uri_check" : "https://keybase.io/{account}",
        "e_code" : 200,
        "e_string" : "class=\"profile-heading\"",
        "m_string" : "<h1>Oy!</h1>",
        "m_code" : 404,
        "known" : ["test", "mubix"],
        "cat" : "social"
       },
       {
        "name" : "Kickstarter",
        "uri_check" : "https://www.kickstarter.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "projects",
        "m_string" : "Oops, Something went missing",
        "m_code" : 404,
        "known" : ["john", "bob"],
        "cat" : "shopping"
       },
       {
        "name" : "kik",
        "uri_check" : "https://kik.me/{account}",
        "e_code" : 200,
        "e_string" : "/thumb.jpg\"/>",
        "m_string" : "<h1 class=\"display-name\"> </h1>",
        "m_code" : 200,
        "known" : ["adam", "smith", "jones"],
        "cat" : "social"
       },
       {
        "name" : "kipin",
        "uri_check" : "https://kipin.app/{account}",
        "e_code" : 200,
        "e_string" : "kipin.app/data/photos/resized2/",
        "m_string" : "Page not found. Link expired, broken or wrong.",
        "m_code" : 302,
        "known" : ["monethica", "asd_fca"],
        "cat" : "business"
       },
       {
        "name" : "KnowYourMeme",
        "uri_check" : "https://knowyourmeme.com/users/{account}",
        "e_code" : 200,
        "e_string" : "Contributions",
        "m_code" : 400,
        "m_string" : "404, File Not Found!",
        "known" : ["ayumukasuga", "butterin-yobread"],
        "cat" : "social"
       },
       {
        "name" : "Ko-Fi",
        "uri_check" : "https://ko-fi.com/{account}",
        "e_code" : 200,
        "e_string" : "id=\"profile-header\"",
        "m_string" : "<title>Object moved</title>",
        "m_code" : 302,
        "known" : ["frank", "marcmakescomics"],
        "cat" : "social",
        "protection" : ["cloudflare"]
       },
       {
        "name" : "komi",
	      "uri_check" : "https://api.komi.io/api/talent/usernames/{account}",
        "uri_pretty" : "https://{account}.komi.io",
        "e_code" : 200,
        "e_string" : "accountStatus\":\"active",
        "m_string" : "The talent profile was not found",
        "m_code" : 404,
        "known" : ["abbysage", "iamdsprings"],
        "cat" : "social"
       },
       {
        "name" : "Kongregate",
        "uri_check" : "https://www.kongregate.com/accounts/{account}",
        "e_code" : 200,
        "e_string" : "Member Since",
        "m_string" : "Sorry, no account with that name was found",
        "m_code" : 404,
        "known" : ["test"],
        "cat" : "gaming"
       },
       {
        "name" : "Kotburger",
        "uri_check" : "https://kotburger.pl/user/{account}",
        "e_code" : 200,
        "e_string" : "Zamieszcza kotburgery od:",
        "m_string" : "Nie znaleziono użytkownika o podanym loginie.",
        "m_code" : 200,
        "known" : ["ania", "janek"],
        "cat" : "images"
       },
       {
         "name" : "Kwai",
         "uri_check" : "https://www.kwai.com/@{account}",
         "e_code" : 200,
         "e_string" : "name=\"title\"",
         "m_string" : "<title>Kwai</title>",
         "m_code" : 200,
         "known" : ["carlito", "taylor"],
         "cat" : "social"
       },
       {
        "name" : "kwejk.pl",
        "uri_check" : "https://kwejk.pl/uzytkownik/{account}#/tablica/",
        "e_code" : 200,
        "e_string" : "Kwejki użytkownika",
        "m_string" : "404 - strona nie została znaleziona - KWEJK.pl",
        "m_code" : 404,
        "known" : ["test", "janek"],
        "cat" : "images"
       },
       {
        "name" : "Kwork",
        "uri_check" : "https://kwork.ru/user_kworks/{account}",
        "uri_pretty" : "https://kwork.ru/user/{account}",
        "post_body" : "{\"username\":\"{account}\",\"offset\":0,\"limit\":10}",
        "e_code" : 200,
        "e_string" : "\"success\":true",
        "m_string" : "\"success\":false",
        "m_code" : 200,
        "known" : ["ilkarkarakurt", "sergeymeshiy"],
        "cat" : "social",
        "headers" : {
            "Content-Type": "application/json"
        }
       },
       {
        "name" : "Lemon8",
        "uri_check" : "https://www.lemon8-app.com/{account}?region=us",
        "e_code" : 200,
        "e_string" : "class=\"user-desc-main-info",
        "m_string" : "unavailableReason\": \"not_found",
        "m_code" : 404,
        "known" : ["phinyamat", "andrianajohnson"],
        "cat" : "social"
       },
       {
        "name" : "LeetCode",
        "uri_check" : "https://leetcode.com/graphql/",
        "uri_pretty" : "https://leetcode.com/u/{account}/",
        "post_body" : "{\"query\":\"query userPublicProfile($username: String!) { matchedUser(username: $username) { username } }\",\"variables\":{\"username\":\"{account}\"},\"operationName\":\"userPublicProfile\"}",
        "e_code" : 200,
        "e_string" : "\"username\":",
        "m_string" : "\"matchedUser\":null",
        "m_code" : 200,
        "known" : ["aku_2000", "wengh"],
        "cat" : "coding",
        "headers" : {
            "Content-Type" : "application/json"
        }
       },
       {
        "name" : "Letterboxd",
        "uri_check" : "https://letterboxd.com/{account}/",
        "e_code" : 200,
        "e_string" : "’s profile on Letterboxd",
        "m_string" : "Sorry, we can’t find the page you’ve requested.",
        "m_code" : 404,
        "known" : ["serdaraltin", "choi"],
        "cat" : "social"
       },
       {
        "name" : "LibraryThing",
        "uri_check" : "https://www.librarything.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "<dt>Joined</dt>",
        "m_string" : "Error: This user doesn't exist",
        "m_code" : 200,
        "known" : ["test", "john"],
        "cat" : "hobby"
       },
       {
        "name" : "Libretooth.gr (Mastodon Instance)",
        "uri_check" : "https://libretooth.gr/api/v1/accounts/lookup?acct={account}",
        "uri_pretty" : "https://libretooth.gr/@{account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_code" : 404,
        "m_string" : "Record not found",
        "known" : ["infolibre", "tzinalilik"],
        "cat" : "social"
       },
       {
        "name" : "lichess.org",
        "uri_check" : "https://lichess.org/api/player/autocomplete?term={account}&exists=1",
        "uri_pretty" : "https://lichess.org/@/{account}",
        "e_code" : 200,
        "e_string" : "true",
        "m_string" : "false",
        "m_code" : 200,
        "known" : ["mohammed01", "mohammed03"],
        "cat" : "gaming"
       },
       {
        "name" : "LINE",
        "uri_check" : "https://line.me/R/ti/p/@{account}?from=page",
        "e_code" : 200,
        "e_string" : "Add LINE Friends via QR Code",
        "m_code" : 404,
        "m_string" : "404 Not Found",
        "known" : [ "roseareal", "yoasobi" ],
        "cat" : "social"
       },
       {
        "name" : "Linktree",
        "uri_check" : "https://linktr.ee/{account}",
        "e_code" : 200,
        "e_string" : "| Linktree",
        "m_string" : "The page you’re looking for doesn’t exist.",
        "m_code" : 404,
        "known" : ["anne", "alex"],
        "cat" : "social"
       },
       {
        "name" : "linux.org.ru",
        "uri_check" : "https://www.linux.org.ru/people/{account}/profile",
        "e_code" : 200,
        "e_string" : "Дата регистрации",
        "m_string" : "Пользователя не существует",
        "m_code" : 404,
        "known" : ["john", "bob"],
        "cat" : "tech"
       },
       {
        "name" : "Livejournal",
        "uri_check" : "https://{account}.livejournal.com",
        "strip_bad_char" : ".",
        "e_code" : 200,
        "e_string" : "<link rel=\"canonical\" href=\"",
        "m_string" : "<title>Unknown Journal",
        "m_code" : 404,
        "known" : ["jill", "john"],
        "cat" : "blog"
       },
       {
        "name" : "livemaster.ru",
        "uri_check" : "https://www.livemaster.ru/{account}",
        "e_code" : 200,
        "e_string" : "<title>Магазин мастера",
        "m_string" : "<title>Вы попали на несуществующую страницу",
        "m_code" : 404,
        "known" : ["redart", "ellentoy"],
        "cat" : "shopping"
       },
       {
        "name" : "lobste.rs",
        "uri_check" : "https://lobste.rs/u/{account}",
        "e_code" : 200,
        "e_string" : "Joined",
        "m_string" : "The resource you requested was not found, or the story has been deleted.",
        "m_code" : 404,
        "known" : ["john", "bob"],
        "cat" : "tech"
       },
       {
        "name" : "Lor.sh (Mastodon Instance)",
        "uri_check" : "https://lor.sh/api/v1/accounts/lookup?acct={account}",
        "uri_pretty" : "https://lor.sh/@{account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_code" : 404,
        "m_string" : "Record not found",
        "known" : ["dump_stack", "lamountain"],
        "cat" : "social"
       },
       {
        "name" : "waytohey",
        "uri_check" : "https://waytohey.com/{account}",
        "e_code" : 200,
        "e_string" : "Send message</span>",
        "m_code" : 404,
        "m_string" : "Unfortunately, this page doesn&#039;t exist.",
        "known" : ["igor", "anna"],
        "cat" : "social"
       },
       {
        "name" : "lowcygier.pl",
        "uri_check" : "https://bazar.lowcygier.pl/user/{account}",
        "e_code" : 200,
        "e_string" : "Zarejestrowany",
        "m_string" : "Błąd 404 - Podana strona nie istnieje",
        "m_code" : 404,
        "known" : ["armin", "janek"],
        "cat" : "gaming"
       },
       {
        "name" : "MAGABOOK",
        "uri_check" : "https://magabook.com/{account}",
        "e_code" : 200,
        "e_string" : "Timeline",
        "m_string" : "",
        "m_code" : 302,
        "known" : ["KristenSuzanne", "mikeflbmer"],
        "cat" : "social"
       },
       {
        "name" : "Magix",
        "uri_check" : "https://www.magix.info/us/users/profile/{account}/",
        "e_code" : 200,
        "e_string" : "About me",
        "m_string" : "Page not found",
        "m_code" : 200,
        "known" : ["baywolfmusic", "johnebaker"],
        "cat" : "music"
       },
       {
        "name" : "MapMyTracks",
        "uri_check" : "https://www.mapmytracks.com/{account}",
        "e_code" : 200,
        "e_string" : "Daily distance this week",
        "m_string" : "Outside together",
        "m_code" : 302,
        "known" : ["ulirad", "CBSloan"],
        "cat" : "health"
       },
       {
        "name" : "Mapstodon.space (Mastodon Instance)",
        "uri_check" : "https://mapstodon.space/api/v1/accounts/lookup?acct={account}",
        "uri_pretty" : "https://mapstodon.space/@{account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_code" : 404,
        "m_string" : "Record not found",
        "known" : ["Autumnhussar", "jeremy"],
        "cat" : "social"
       },
       {
        "name" : "Maroc_nl",
        "uri_check" : "https://www.maroc.nl/forums/members/{account}.html",
        "e_code" : 200,
        "e_string" :"Bekijk Profiel:",
        "m_string" : "Deze gebruiker is niet geregistreerd",
        "m_code" : 200,
        "known" : ["brahim", "brahim01"],
        "cat" : "social"
       },
       {
        "name" : "Marshmallow",
        "uri_check" : "https://marshmallow-qa.com/{account}",
        "e_code" : 200,
        "e_string" : "さんにメッセージをおくる",
        "m_string" : "For compensation, here are cats for you.",
        "m_code" : 404,
        "known" : ["yuino_fox", "momo"],
        "cat" : "social"
       },
       {
        "name" : "Martech",
        "uri_check" : "https://martech.org/author/{account}/",
        "e_code" : 200,
        "e_string" : "twitter:site",
        "m_string" : "Page not found",
        "m_code" : 404,
        "known" : ["mani-karthik", "james-green"],
        "cat" : "business"
       },
       {
        "name" : "Massage Anywhere",
        "uri_check" : "https://www.massageanywhere.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "<title>MassageAnywhere.com Profile for ",
        "m_string" : "<title>MassageAnywhere.com: Search Results</title>",
        "m_code" : 200,
        "known" : ["lorilmccluskey", "LomiNYC"],
        "cat" : "health"
       },
       {
        "name" : "masto.ai",
        "uri_check" : "https://masto.ai/@{account}",
        "e_code" : 200,
        "e_string" : "@masto.ai) - Mastodon</title>",
        "m_string" : "The page you are looking for isn&#39;t here.",
        "m_code" : 404,
        "known" : ["rbreich", "stux"],
        "cat" : "social"
       },
       {
        "name" : "Masto.nyc (Mastodon Instance)",
        "uri_check" : "https://masto.nyc/api/v1/accounts/lookup?acct={account}",
        "uri_pretty" : "https://masto.nyc/@{account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_code" : 404,
        "m_string" : "Record not found",
        "known" : ["seano", "jayjay718"],
        "cat" : "social"
       },
       {
        "name" : "Mastodonbooks.net (Mastodon Instance)",
        "uri_check" : "https://mastodonbooks.net/api/v1/accounts/lookup?acct={account}",
        "uri_pretty" : "https://mastodonbooks.net/@{account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_code" : 404,
        "m_string" : "Record not found",
        "known" : ["RogerRemacle", "eugnick"],
        "cat" : "social"
       },
       {
        "name" : "Mastodon-mastodon",
        "uri_check" : "https://mastodon.social/@{account}",
        "e_code" : 200,
        "e_string" : "profile:username",
        "m_string" : "The page you are looking for isn't here.",
        "m_code" : 404,
        "known" : ["john", "alex"],
        "cat" : "social"
       },
       {
        "name" : "Mastodon API",
        "uri_check" : "https://mastodon.social/api/v2/search?q={account}&limit=1&type=accounts",
        "uri_pretty" : "https://mastodon.social/api/v2/search?q={account}&type=accounts",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_string" : "\"accounts\":[]",
        "m_code" : 404,
        "known" : ["Richard_Littler", "webbreacher"],
        "cat" : "social"
       },
       {
        "name" : "Mastodon.online",
        "uri_check" : "https://mastodon.online/@{account}",
        "e_code" : 200,
        "e_string" : "@mastodon.online) - Mastodon</title>",
        "m_string" : "<title>The page you are looking for isn&#39;t here.",
        "m_code" : 404,
        "known" : ["Gargron", "RDHale"],
        "cat" : "social"
       },
       {
        "name" : "Mastodon-Toot.Community",
        "uri_check" : "https://toot.community/@{account}",
        "e_code" : 200,
        "e_string" : "@toot.community) - toot.community</title>",
        "m_string" : "The page you are looking for isn&#39;t here.",
        "m_code" : 404,
        "known" : ["Johnny", "jorijn"],
        "cat" : "social"
       },
       {
        "name" : "Mastodon-climatejustice.rocks",
        "uri_check" : "https://climatejustice.rocks/api/v1/accounts/lookup?acct={account}",
        "uri_pretty" : "https://climatejustice.rocks/@{account}",
        "e_code" : 200,
        "e_string" : "username\":",
        "m_string" : "Record not found",
        "m_code" : 404,
        "known" : ["paula", "PaulaToThePeople"],
        "cat" : "social"
       },
       {
        "name" : "Mastodon-C.IM",
        "uri_check" : "https://c.im/@{account}",
        "e_code" : 200,
        "e_string" : "@c.im) - C.IM</title>",
        "m_string" : "<title>The page you are looking for isn&#39;t here",
        "m_code" : 404,
        "known" : ["admin", "paidugroup"],
        "cat" : "social"
       },
       {
        "name" : "MCName (Minecraft)",
        "uri_check" : "https://mcname.info/en/search?q={account}",
        "e_code" : 200,
        "e_string" : "card mb-3 text-monospace",
        "m_string" : "alert alert-success px-0 py-1",
        "m_code" : 200,
        "known" : ["unrevive", "nxtuny"],
        "cat" : "gaming"
       },
       {
        "name" : "MCUUID (Minecraft)",
        "uri_check" : "https://playerdb.co/api/player/minecraft/{account}",
        "uri_pretty" : "https://mcuuid.net/?q={account}",
        "e_code" : 200,
        "e_string" : "Successfully found player by given ID.",
        "m_string" : "minecraft.api_failure",
        "m_code" : 200,
        "known" : ["smithy", "bob"],
        "cat" : "gaming"
       },
       {
        "name" : "Medium",
        "uri_check" : "https://{account}.medium.com/about",
        "strip_bad_char" : ".",
        "e_code" : 200,
        "e_string" : "Medium member since",
        "m_string" : "Out of nothing, something",
        "m_code" : 404,
        "known" : ["zulie", "jessicalexicus"],
        "cat" : "news"
       },
       {
        "name" : "medyczka.pl",
        "uri_check" : "http://medyczka.pl/user/{account}",
        "e_code" : 200,
        "e_string" : "Lista uzytkownikow",
        "m_string" : "This user has not registered and therefore does not have a profile to view.",
        "m_code" : 200,
        "known" : ["test", "janek"],
        "cat" : "health"
       },
       {
        "name" : "meet me",
        "uri_check" : "https://www.meetme.com/{account}",
        "e_code" : 200,
        "e_string" : "<title>Meet people like ",
        "m_string" : "<title>MeetMe - Chat and Meet New People</title",
        "m_code" : 302,
        "known" : ["john", "marsha"],
        "cat" : "dating"
       },
       {
        "name" : "Mastodon-meow.social",
        "uri_check" : "https://meow.social/@{account}",
        "e_code" : 200,
        "e_string" : "- the mastodon instance for creatures fluffy, scaly and otherwise</title>",
        "m_string" : "The page you are looking for isn&#39;t here.",
        "m_code" : 404,
        "known" : ["meow", "novra"],
        "cat" : "social"
       },
       {
        "name" : "message_me",
        "uri_check" : "https://mssg.me/{account}",
        "e_code" : 200,
        "e_string" : "_id",
        "m_string" : "<title>404</title>",
        "m_code" : 404,
        "known" : ["sue", "david"],
        "cat" : "social"
       },
       {
        "name" : "metacritic",
        "uri_check" : "https://www.metacritic.com/user/{account}",
        "e_code" : 200,
        "e_string" : "'s Profile - Metacritic",
        "m_string" : "<title>Sign up to get your own profile - Metacritic</",
        "m_code" : 200,
        "known" : ["dev", "matt"],
        "cat" : "hobby"
       },
       {
        "name" : "Minds",
        "uri_check" : "https://www.minds.com/{account}/",
        "e_code" : 200,
        "e_string" : ") | Minds</title>",
        "m_string" : "Sorry, this channel doesn't appear to exist",
        "m_code" : 404,
        "known" : ["Willieleev1971", "john"],
        "cat" : "political"
       },
       {
        "name" : "Minecraft List",
        "uri_check" : "https://minecraftlist.com/players/{account}",
        "e_code" : 200,
        "e_string" : "-->was seen on<!--",
        "m_string" : "0 Minecraft servers recently",
        "m_code" : 200,
        "known" : ["fear837", "dream"],
        "cat" : "gaming"
       },
       {
        "name" : "mintme",
        "uri_check" : "https://www.mintme.com/token/{account}",
        "e_code" : 200,
        "e_string" : "token | mintMe",
        "m_string" : "Page not found",
        "m_code" : 404,
        "known" : ["john", "crypto"],
        "cat" : "finance"
       },
       {
        "name" : "Mistrzowie",
        "uri_check" : "https://mistrzowie.org/user/{account}",
        "e_code" : 200,
        "e_string" : "Profil użytkownika",
        "m_string" : "Nie znaleziono użytkownika o podanym loginie.",
        "m_code" : 200,
        "known" : ["test", "janek"],
        "cat" : "images"
       },
       {
        "name" : "Mix",
        "uri_check" : "https://mix.com/{account}/",
        "e_code" : 200,
        "e_string" : "<title>@",
        "m_string" : "The best content from the open web, personalized.",
        "m_code" : 302,
        "known" : ["test", "mixpicks"],
        "cat" : "social"
       },
       {
        "name" : "Mixcloud",
        "uri_check" : "https://api.mixcloud.com/{account}/",
        "uri_pretty" : "https://www.mixcloud.com/{account}/",
        "e_code" : 200,
        "e_string" : "\"username\":",
        "m_string" : "\"error\":",
        "m_code" : 404,
        "known" : ["DjHunnyBee", "vegarecords"],
        "cat" : "music"
       },
       {
        "name" : "Mixi",
        "uri_check" : "https://mixi.jp/view_community.pl?id={account}",
        "e_code" : 200,
        "e_string" : "| mixiコミュニティ</title>",
        "m_string" : "データがありません",
        "m_code" : 200,
        "known" : ["2854333", "19123"],
        "cat" : "social"
       },
       {
        "name" : "Mixlr",
        "uri_check" : "http://api.mixlr.com/users/{account}",
        "uri_pretty" : "http://mixlr.com/{account}/",
        "e_code" : 200,
        "e_string" : "username",
        "m_string" : "Resource not found",
        "m_code" : 404,
        "known" : ["test", "john"],
        "cat" : "music"
       },
       {
        "name" : "Mmorpg",
        "uri_check" : "https://forums.mmorpg.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "MMORPG.com Forums",
        "m_string" : "404 Not Not_Found",
        "m_code" : 404,
        "known" : ["TheDalaiBomba", "MadLovin"],
        "cat" : "gaming"
       },
       {
        "name" : "MobileGTA.net",
        "uri_check" : "https://www.mobilegta.net/en/user/{account}",
        "e_code" : 200,
        "e_string" : "userpage_user",
        "m_string" : "<h1>404 Not Found",
        "m_code" : 200,
        "known" : ["daniel", "franco"],
        "cat" : "gaming"
       },
       {
        "name" : "Monkeytype",
        "uri_check" : "https://api.monkeytype.com/users/{account}/profile",
        "uri_pretty" : "https://monkeytype.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "\"message\":\"Profile retrieved\"",
        "m_string" : "\"message\":\"User not found\"",
        "m_code" : 404,
        "known" : ["rocket", "risenrelic"],
        "cat" : "coding"
       },
       {
        "name" : "MODX.im",
        "uri_check" : "https://modx.evo.im/profile/{account}/",
        "e_code" : 200,
        "e_string" : "class=\"profile\"",
        "m_string" : "class=\"content-error\"",
        "m_code" : 404,
        "known" : ["Grinyaha", "kymage"],
        "cat" : "tech"
       },
       {
        "name" : "Mod DB",
        "uri_check" : "https://www.moddb.com/members/{account}",
        "e_code" : 200,
        "e_string" : "joined <time",
        "m_string" : "Login is required to view the requested member profile",
        "m_code" : 403,
        "known" : ["sprinklesoup", "emargy"],
        "cat" : "gaming"
       },
       {
        "name" : "Motokiller",
        "uri_check" : "https://mklr.pl/user/{account}",
        "e_code" : 200,
        "e_string" : "Zamieszcza materiały od:",
        "m_string" : "Nie znaleziono użytkownika o podanym loginie.",
        "m_code" : 200,
        "known" : ["test", "janek"],
        "cat" : "images"
       },
        {
        "name" : "Moto Trip",
        "uri_check" : "https://moto-trip.com/profil/{account}",
        "e_code" : 200,
        "e_string" : "<h1 class=\"h2\">Profil de ",
        "m_string" : "<h1>Page introuvable</h1>",
        "m_code" : 404,
        "known" : ["aesthetics", "pif"],
        "cat" : "hobby"
       },
       {
        "name" : "moxfield",
        "uri_check" : "https://www.moxfield.com/users/{account}",
        "e_code" : 200,
        "e_string" : "Moxfield Profile",
        "m_string" : "No user found ",
        "m_code" : 200,
        "known" : ["gamer", "Carlos01"],
        "cat" : "misc"
       },
       {
        "name" : "Mastodon-mstdn.io",
        "uri_check" : "https://mstdn.io/@{account}",
        "e_code" : 200,
        "e_string" : "@mstdn.io) - Mastodon",
        "m_string" : "The page you are looking for isn&#39;t here.",
        "m_code" : 404,
        "known" : ["mike", "greg"],
        "cat" : "social"
       },
       {
        "name" : "Muck Rack",
        "uri_check" : "https://muckrack.com/{account}",
        "e_code" : 200,
        "e_string" : "on Muck Rack",
        "m_string" : "Oh no! Page not found.",
        "m_code" : 404,
        "known" : ["john"],
        "cat" : "news"
       },
       {
        "name" : "Musician.social (Mastodon Instance)",
        "uri_check" : "https://musician.social/api/v1/accounts/lookup?acct={account}",
        "uri_pretty" : "https://musician.social/@{account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_code" : 404,
        "m_string" : "Record not found",
        "known" : ["Alizar", "weisjohan"],
        "cat" : "social"
       },
       {
        "name" : "musictraveler",
        "uri_check" : "https://www.musictraveler.com/en/users/{account}/",
        "e_code" : 200,
        "e_string" : "on Music Traveler</title>",
        "m_string" : "<title>Page Not found</title>",
        "m_code" : 404,
        "known" : ["dave", "sarah"],
        "cat" : "music"
       },
       {
        "name" : "MUYZORRAS",
        "uri_check" : "https://www.muyzorras.com/usuarios/{account}",
        "e_code" : 200,
        "e_string" : "og:title",
        "m_string" : "<title>Error 404",
        "m_code" : 404,
        "known" : ["anuel", "esteban"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "myWishBoard",
        "uri_check" : "https://mywishboard.com/@{account}",
        "e_code" : 200,
        "e_string" : "class=\"MwbUserHeader\"",
        "m_string" : "class=\"MwbError\"",
        "m_code" : 404,
        "known" : ["ke7_2024", "alekseevvasil"],
        "cat" : "shopping"
       },
       {
        "name" : "MyAnimeList",
        "uri_check" : "https://myanimelist.net/profile/{account}",
        "e_code" : 200,
        "e_string" : "Profile - MyAnimeList.net",
        "m_string" : "<title>404 Not Found",
        "m_code" : 404,
        "known" : ["test", "admin"],
        "cat" : "social"
       },
       {
        "name" : "MyBuilder.com",
        "uri_check" : "https://www.mybuilder.com/profile/view/{account}",
        "e_code" : 200,
        "e_string" : "feedback",
        "m_string" : "Whoops! You broke our site!",
        "m_code" : 404,
        "known" : ["blue", "john"],
        "cat" : "social"
       },
       {
        "name" : "MyFitnessPal Author",
        "uri_check" : "https://blog.myfitnesspal.com/author/{account}/",
        "e_code" : 200,
        "e_string" : "About the Author",
        "m_string" : "<title>Page not found ",
        "m_code" : 404,
        "known" : ["lauren-krouse", "julia-malacoff"],
        "cat" : "health"
       },
       {
        "name" : "MyFitnessPal Community",
        "uri_check" : "https://community.myfitnesspal.com/en/profile/{account}",
        "e_code" : 200,
        "e_string" : ">Last Active<",
        "m_string" : "User Not Found",
        "m_code" : 404,
        "known" : ["malibu927", "L1zardQueen"],
        "cat" : "health"
       },
       {
        "name" : "mymfans",
        "uri_check" : "https://mym.fans/{account}",
        "e_code" : 200,
        "e_string" : " • MYM</title>",
        "m_string" : "• MYM • Exclusive social network for creators &amp; fans</title>",
        "m_code" : 404,
        "known" : ["Unmissabl", "Lalogebeaute"],
        "cat" : "social"
       },
       {
        "name" : "my_instants",
        "uri_check" : "https://www.myinstants.com/en/profile/{account}/",
        "e_code" : 200,
        "e_string" : " | Myinstants</title>",
        "m_string" : "Page not found",
        "m_code" : 404,
        "known" : ["daniel01", "dave"],
        "cat" : "music"
       },
       {
        "name" : "MyLot",
        "uri_check" : "https://www.mylot.com/{account}",
        "e_code" : 200,
        "e_string" : "on myLot</title>",
        "m_string" : " / Whoops!",
        "m_code" : 404,
        "known" : ["Tampa_girl7"],
        "cat" : "social"
       },
       {
        "name" : "mym.fans",
        "uri_check" : "https://mym.fans/{account}",
        "e_code" : 200,
        "e_string" : "posts",
        "m_string" : "Il n’y a rien ici…",
        "m_code" : 404,
        "known" : ["Djelizamay","Andysparkles"],
        "cat" : "social"
       },
       {
        "name" : "myportfolio",
        "uri_check" : "https://{account}.myportfolio.com/work",
        "strip_bad_char" : ".",
        "e_code" : 200,
        "e_string" : "class=\"page-title",
        "m_string" : "<title>Adobe Portfolio | Build your own personalized website</title>",
        "m_code" : 302,
        "known" : ["artkonina", "fox"],
        "cat" : "misc"
       },
       {
        "name" : "MySpace",
        "uri_check" : "https://myspace.com/{account}",
        "e_code" : 200,
        "e_string" : "<!-- Profile -->",
        "m_string" : "<!-- 404 -->",
        "m_code" : 404,
        "known" : ["alice", "bob"],
        "cat" : "social"
       },
       {
        "name" : "Myspreadshop",
        "uri_check" : "https://myspreadshop.de/{account}/shopData/list",
        "uri_pretty" : "https://{account}.myspreadshop.com",
        "e_code" : 200,
        "e_string" : "siteName",
        "m_code" : 404,
        "m_string" : "not found",
        "known" : ["arukori", "honey"],
        "cat" : "business"
       },
       {
        "name" : "naija_planet",
        "uri_check" : "https://naijaplanet.com/{account}",
        "e_code" : 200,
        "e_string" : "dating Profile, ",
        "m_string" : "- NaijaPlanet!",
        "m_code" : 200,
        "known" : ["daniel01", "wales73"],
        "cat" : "dating"
       },
       {
        "name" : "nairaland",
        "uri_check" : "https://www.nairaland.com/{account}",
        "e_code" : 200,
        "e_string" : "s Profile",
        "m_string" : "404: Page Not Found",
        "m_code" : 301,
        "known" : ["amakaone", "seun"],
        "cat" : "news"

       },
       {
        "name" : "NaturalNews",
        "uri_check" : "https://naturalnews.com/author/{account}/",
        "e_code" : 200,
        "e_string" : "All posts by",
        "m_string" : "The page you are looking for cannot be found or is no longer available.",
        "m_code" : 200,
        "known" : ["jdheyes", "healthranger"],
        "cat" : "political"
       },
       {
        "name" : "Naver",
        "uri_check" : "https://blog.naver.com/{account}",
        "e_code" : 200,
        "e_string" : " : 네이버 블로그",
        "m_string" : "페이지를 찾을 수 없습니다",
        "m_code" : 500,
        "known" : ["bob", "blue"],
        "cat" : "social"
       },
       {
        "name" : "Neocities",
        "uri_check" : "https://neocities.org/site/{account}",
        "e_code" : 200,
        "e_string" : "noindex, follow",
        "m_string" : "- Not Found</title>",
        "m_code" : 404,
        "known" : ["fauux", "sadgrl"],
        "cat" : "social"
       },
       {
        "name" : "netvibes",
        "uri_check" : "https://www.netvibes.com/{account}",
        "e_code" : 200,
        "e_string" : "userId",
        "m_string" : "Page not found",
        "m_code" : 404,
        "known" : ["nebkacrea", "cdiljda"],
        "cat" : "social"
       },
       {
        "name" : "Newgrounds",
        "uri_check" : "https://{account}.newgrounds.com/",
        "strip_bad_char" : ".",
        "e_code" : 200,
        "e_string" : "user-header-name",
        "m_string" : "Whoops, that's a swing and a miss!",
        "m_code" : 404,
        "known" : ["john", "bob"],
        "cat" : "gaming"
       },
       {
        "name" : "newmeet",
        "uri_check" : "https://www.newmeet.com/en/profile/{account}/",
        "e_code" : 200,
        "e_string" : "<h2>The profile of",
        "m_string" : "Chat with , , ,  - ",
        "m_code" : 200,
        "known" : ["Harmonie06", "Bach007"],
        "cat" : "dating"
       },
       {
        "name" : "nihbuatjajan",
        "uri_check" : "https://www.nihbuatjajan.com/{account}",
        "e_code" : 200,
        "e_string" : ") | Nih buat jajan</title>",
        "m_string" : "<title>Nih Buat Jajan</title>",
        "m_code" : 302,
        "known" : ["banyusadewa", "danirachmat"],
        "cat" : "social"
       },
       {
        "name" : "npm",
        "uri_check" : "https://www.npmjs.com/~{account}",
        "e_code" : 200,
        "e_string" : "/npm-avatar/",
        "m_string" : "poster depicting npm&#x27;s mascot wombat",
        "m_code" : 404,
        "known" : ["npm", "rich_harris"],
        "cat" : "coding"
       },
       {
        "name" : "Nitecrew (Mastodon Instance)",
        "uri_check" : "https://nitecrew.rip/api/v1/accounts/lookup?acct={account}",
        "uri_pretty" : "https://nitecrew.rip/@{account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_code" : 404,
        "m_string" : "Record not found",
        "known" : ["Myxx", "honey"],
        "cat" : "social"
       },
       {
        "name" : "nnru",
        "uri_check" : "https://{account}.www.nn.ru",
        "strip_bad_char" : ".",
        "e_code" : 200,
        "e_string" : "<title> ",
        "m_string" : "<title>Ошибка 404 -",
        "m_code" : 404,
        "known" : ["lena", "slava"],
        "cat" : "social"
       },
       {
        "name" : "NotABug",
        "uri_check" : "https://notabug.org/{account}",
        "e_code" : 200,
        "e_string" : "followers and is following",
        "m_string" : "Not Found",
        "m_code" : 404,
        "known" : ["notabug", "hp", "zPlus"],
        "cat" : "coding"
       },
       {
        "name" : "Note",
        "uri_check" : "https://note.com/{account}",
        "e_code" : 200,
        "e_string" : "フォロワー",
        "m_code" : 404,
        "m_string" : "お探しのページが見つかりません。",
        "known" : ["honey", "yui"],
        "cat" : "social"
       },
       {
        "name" : "OnlySearch (OnlyFans)",
        "uri_check" : "https://onlysearch.co/api/search?keyword={account}",
        "uri_pretty" : "https://onlysearch.co/profiles?keyword={account}",
        "e_code" : 200,
        "e_string" : "\"hits\":[{",
        "m_string" : "\"hits\":[]",
        "m_code" : 200,
        "known" : ["miaimani", "milaamour"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "oglaszamy24h.pl",
        "uri_check" : "https://oglaszamy24h.pl/profil,{account}",
        "e_code" : 200,
        "e_string" : "Profil użytkownika:",
        "m_string" : "Nieprawidłowy link, w bazie danych nie istnieje użytkownik o podanym loginie",
        "m_code" : 404,
        "known" : ["kowal", "janek"],
        "cat" : "shopping"
       },
       {
        "name" : "ok.ru",
        "uri_check" : "https://ok.ru/{account}",
        "e_code" : 200,
        "e_string" : "| OK",
        "m_string" : "class=\"p404_t",
        "m_code" : 404,
        "known" : ["john", "aleksandrvasillev"],
        "cat" : "social"
       },
       {
        "name" : "okidoki",
        "uri_check" : "https://m.okidoki.ee/ru/users/{account}/",
        "e_code" : 200,
        "e_string" : "Пользователь",
        "m_string" : "Страница не найдена",
        "m_code" : 404,
        "known" : ["nastya3", "nastya"],
        "cat" : "misc"
       },
       {
        "name" : "Opencollective",
        "uri_check" : "https://opencollective.com/{account}",
        "e_code" : 200,
        "e_string" : "- Open Collective",
        "m_string" : "Not Found",
        "m_code" : 200,
        "known" : ["john", "bob"],
        "cat" : "finance"
       },
       {
        "name" : "opensource",
        "uri_check" : "https://opensource.com/users/{account}",
        "e_code" : 200,
        "e_string" : "| Opensource.com",
        "m_string" : "Page not found",
        "m_code" : 404,
        "known" : ["dave", "mike"],
        "cat" : "tech"
       },
       {
        "name" : "OpenStreetMap",
        "uri_check" : "https://www.openstreetmap.org/user/{account}",
        "e_code" : 200,
        "e_string" : "Mapper since:",
        "m_string" : "does not exist",
        "m_code" : 404,
        "known" : ["kemkim"],
        "cat" : "social"
       },
       {
        "name" : "OPGG",
        "uri_check" : "https://eune.op.gg/summoners/eune/{account}",
        "e_code" : 200,
        "e_string" : "- Summoner Stats - League of Legends",
        "m_string" : "Guide - OP.GG",
        "m_code" : 200,
        "known" : ["xin", "carlos01"],
        "cat" : "gaming"
       },
       {
        "name" : "Orbys",
        "uri_check" : "https://orbys.net/{account}",
        "e_code" : 200,
        "e_string" : "profile_user_image",
        "m_string" : "The page you are looking for cannot be found.",
        "m_code" : 404,
        "known" : ["txmustang302"],
        "cat" : "social"
       },
       {
        "name" : "Origins.Habbo.com",
        "uri_check" : "https://origins.habbo.com/api/public/users?name={account}",
        "e_code" : 200,
        "e_string" : "uniqueId",
        "m_string" : "not-found",
        "m_code" : 404,
        "known" : ["john", "jane"],
        "cat" : "gaming"
       },
       {
        "name" : "Origins.Habbo.com.br",
        "uri_check" : "https://origins.habbo.com.br/api/public/users?name={account}",
        "e_code" : 200,
        "e_string" : "uniqueId",
        "m_string" : "not-found",
        "m_code" : 404,
        "known" : ["carlos", "pedro"],
        "cat" : "gaming"
       },
       {
        "name" : "Origins.Habbo.es",
        "uri_check" : "https://origins.habbo.es/api/public/users?name={account}",
        "e_code" : 200,
        "e_string" : "uniqueId",
        "m_string" : "not-found",
        "m_code" : 404,
        "known" : ["carlos", "mary"],
        "cat" : "gaming"
       },
       {
        "name" : "osu!",
        "uri_check" : "https://osu.ppy.sh/users/{account}",
        "e_code" : 302,
        "e_string" : "",
        "m_string" : "User not found! ;_;",
        "m_code" : 404,
        "known" : ["stretches", "spiken8"],
        "cat" : "gaming"
       },
       {
        "name" : "Our Freedom Book",
        "uri_check" : "https://www.ourfreedombook.com/{account}",
        "e_code" : 200,
        "e_string" : "meta property=\"og:",
        "m_string" : "Sorry, page not found",
        "m_code" : 302,
        "known" : ["DaveLipsky", "StarlaJene"],
        "cat" : "social"
       },
       {
        "name" : "ow.ly",
        "uri_check" : "http://ow.ly/user/{account}",
        "e_code" : 200,
        "e_string" : "Images",
        "m_string" : "404 error",
        "m_code" : 404,
        "known" : ["StopAdMedia", "jokervendetti"],
        "cat" : "social"
       },
       {
        "name" : "palnet",
        "uri_check" : "https://www.palnet.io/@{account}/",
        "e_code" : 200,
        "e_string" : "class=\"profile-cover\"",
        "m_string" : "Unknown user account!",
        "m_code" : 404,
        "known" : ["trincowski-pt", "anggreklestari"],
        "cat" : "social"
       },
       {
        "name" : "Parler",
        "uri_check" : "https://parler.com/user/{account}",
        "e_code" : 200,
        "e_string" : "People to Follow",
        "m_string" : "join Parler today",
        "m_code" : 302,
        "known" : ["DineshDsouza", "SeanHannity"],
        "cat" : "social"
       },
       {
        "name" : "Parler archived profile",
        "uri_check" : "http://archive.org/wayback/available?url=https://parler.com/profile/{account}",
        "uri_pretty" : "https://web.archive.org/web/2/https://parler.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "\"archived_snapshots\": {\"closest\"",
        "m_string" : "\"archived_snapshots\": {}",
        "m_code" : 200,
        "known" : ["JoePags", "dineshdsouza"],
        "cat" : "archived"
       },
       {
        "name" : "Parler archived posts",
        "uri_check" : "http://archive.org/wayback/available?url=https://parler.com/profile/{account}/posts",
        "uri_pretty" : "https://web.archive.org/web/2/https://parler.com/profile/{account}/posts",
        "e_code" : 200,
        "e_string" : "\"archived_snapshots\": {\"closest\"",
        "m_string" : "\"archived_snapshots\": {}",
        "m_code" : 200,
        "known" : ["JoePags", "dineshdsouza"],
        "cat" : "archived"
       },
       {
        "name" : "Pastebin",
        "uri_check" : "https://pastebin.com/u/{account}",
        "e_code" : 200,
        "e_string" : "'s Pastebin",
        "m_string" : "",
        "m_code" : 404,
        "known" : ["test", "john"],
        "cat" : "tech"
       },
       {
        "name" : "patch",
        "uri_check" : "https://patch.com/users/{account}",
        "e_code" : 200,
        "e_string" : "<title>Patch User Profile",
        "m_string" : "<title>Page not found</title>",
        "m_code" : 404,
        "known" : ["dave", "bob"],
        "cat" : "news"
       },
       {
        "name" : "PatientsLikeMe",
        "uri_check" : "https://www.patientslikeme.com/members/{account}",
        "e_code" : 200,
        "e_string" : "s profile | PatientsLikeMe</title>",
        "m_string" : "",
        "m_code" : 302,
        "known" : ["thjuland", "Pedro0703", "Hydropioneer"],
        "cat" : "health"
       },
       {
        "name" : "Patreon",
        "uri_check" : "https://www.patreon.com/{account}",
        "e_code" : 200,
        "e_string" : "full_name\":",
        "m_string" : "errorCode\": 404,",
        "m_code" : 404,
        "known" : ["mubix", "doughboys"],
        "cat" : "finance"
       },
       {
        "name" : "Patriots Win",
        "uri_check" : "https://patriots.win/u/{account}/",
        "e_code" : 200,
        "e_string" : "nav-user active register",
        "m_string" : "An error occurred",
        "m_code" : 500,
        "known" : ["r3deleven", "MemeFactory"],
        "cat" : "political"
       },
       {
        "name" : "Patronite",
        "uri_check" : "https://patronite.pl/{account}",
        "e_code" : 200,
        "e_string" : "Zostań Patronem",
        "m_string" : "Nie znaleźliśmy strony której szukasz.",
        "m_code" : 404,
        "known" : ["radio357", "radionowyswiat"],
        "cat" : "finance"
        },
        {
        "name" : "Paypal",
        "uri_check" : "https://www.paypal.com/paypalme/{account}",
        "e_code" : 200,
        "e_string" : "userInfo",
        "m_string" : "<title>PayPal.Me</title><meta",
        "m_code" : 200,
        "known" : ["OCMermaid", "blackrock"],
        "cat" : "finance"
       },
       {
        "name" : "PCGamer",
        "uri_check" : "https://forums.pcgamer.com/members/{account}/",
        "e_code" : 200,
        "e_string" : "Joined",
        "m_string" : "Oops! We ran into some problems",
        "m_code" : 404,
        "known" : ["volley.302", "cjmariani.94198", "cholidsnake.2334"],
        "cat" : "gaming"
       },
       {
        "name" : "PCPartPicker",
        "uri_check" : "https://pcpartpicker.com/user/{account}/",
        "e_code" : 200,
        "e_string" : "class=\"active\"",
        "m_string" : "The page you requested could not be found.",
        "m_code" : 404,
        "known" : ["john", "bob"],
        "cat" : "tech"
       },
       {
        "name" : "Peing",
        "uri_check" : "https://peing.net/api/v2/items/?type=answered&account={account}",
        "uri_pretty" : "https://peing.net/{account}",
        "e_code" : 200,
        "e_string" : "items",
        "m_code" : 404,
        "m_string" : "Not Found",
        "known" : ["honey", "blink"],
        "cat" : "social"
       },
       {
        "name" : "Periscope",
        "uri_check" : "https://www.periscope.tv/{account}",
        "e_code" : 200,
        "e_string" : "<label>Followers",
        "m_string" : "Sorry, this page doesn’t exist",
        "m_code" : 404,
        "known" : ["john", "test"],
        "cat" : "video"
       },
       {
        "name" : "Pewex",
        "uri_check" : "https://retro.pewex.pl/user/{account}",
        "e_code" : 200,
        "e_string" : "Zamieszcza eksponaty od:",
        "m_string" : "Nie znaleziono użytkownika o podanym loginie.",
        "m_code" : 200,
        "known" : ["test", "ania"],
        "cat" : "misc"
       },
       {
        "name" : "Picsart",
        "uri_check" : "https://picsart.com/u/{account}",
        "e_code" : 200,
        "e_string" : "Profiles on Picsart",
        "m_string" : "User not found",
        "m_code" : 404,
        "known" : ["john", "john404"],
        "cat" : "art"
       },
       {
        "name" : "Piekielni",
        "uri_check" : "https://piekielni.pl/user/{account}",
        "e_code" : 200,
        "e_string" : "Zamieszcza historie od:",
        "m_string" : "Nie znaleziono użytkownika o podanym loginie.",
        "m_code" : 200,
        "known" : ["test", "janek"],
        "cat" : "misc"
       },
       {
        "name" : "pikabu",
        "uri_check" : "https://pikabu.ru/@{account}",
        "e_code" : 200,
        "e_string" : "— все посты пользователя",
        "m_string" : "404. Страница не найдена",
        "m_code" : 404,
        "known" : ["igor01", "serguei"],
        "cat" : "social"
       },
       {
        "name" : "Pillowfort",
        "uri_check" : "https://www.pillowfort.social/{account}",
        "e_code" : 200,
        "e_string" : "<meta property=\"og:site_name\" content=\"Pillowfort\">",
        "m_code" : 404,
        "m_string" : "That page does not exist, or you do not have the proper permissions to view it.",
        "known" : ["MissMoonified", "honey"],
        "cat" : "social"
       },
       {
        "name" : "PinkBike",
        "uri_check" : "https://www.pinkbike.com/u/{account}/",
        "e_code" : 200,
        "e_string" : "on Pinkbike</title>",
        "m_string" : "I couldn't find the page you were looking for",
        "m_code" : 404,
        "known" : ["whistlermountainbikepark", "paulhanson"],
        "cat" : "hobby"
       },
       {
        "name" : "Pinterest",
        "uri_check" : "https://www.pinterest.com/{account}/",
        "e_code" : 200,
        "e_string" : " - Profile | Pinterest",
        "m_string" : "Whoops! We couldn't find that page",
        "m_code" : 404,
        "known" : ["test123", "frickcollection"],
        "cat" : "social"
       },
       {
        "name" : "pixelfed.social",
        "uri_check" : "https://pixelfed.social/{account}",
        "e_code" : 200,
        "e_string" : "on pixelfed</title>",
        "m_string" : "<title>pixelfed</title>",
        "m_code" : 404,
        "known" : ["sarah", "john"],
        "cat" : "social"
       },
       {
        "name" : "Playstation Network",
        "uri_check" : "https://psnprofiles.com/xhr/search/users?q={account}",
        "e_code" : 200,
        "e_string" : "<div class=\"progress-bar small level\">",
        "m_string" : "We couldn't find anything ",
        "m_code" : 200,
        "known" : ["SlimShaggy18", "ikemenzi"],
        "cat" : "gaming"
       },
       {
        "name" : "Plurk",
        "uri_check" : "https://www.plurk.com/{account}",
        "e_code" : 200,
        "e_string" : "Profile views",
        "m_string" : "Register your plurk account",
        "m_code" : 200,
        "known" : ["test"],
        "cat" : "social"
       },
       {
       "name" : "Pokec",
       "uri_check" : "https://pokec.azet.sk/{account}",
       "e_code" : 200,
       "e_string" :"idReportedUser",
       "m_string" : "Neexistujúci používateľ",
       "m_code" : 404,
       "known" : ["tobias", "brahim1"],
       "cat" : "social"
       },
       {
        "name" : "pokemonshowdown",
        "uri_check" : "https://pokemonshowdown.com/users/{account}",
        "e_code" : 200,
        "e_string" : "Official ladder",
        "m_string" : " (Unregistered)",
        "m_code" : 404,
        "known" : ["red", "blue"],
        "cat" : "gaming"
       },
       {
        "name" : "Pokerstrategy",
        "uri_check" : "http://www.pokerstrategy.net/user/{account}/profile/",
        "e_code" : 200,
        "e_string" : "User profile for",
        "m_string" : "Sorry, the requested page couldn't be found!",
        "m_code" : 404,
        "known" : ["john", "bob"],
        "cat" : "gaming"
       },
       {
        "name" : "Polchat.pl",
        "uri_check" : "https://polczat.pl/forum/profile/{account}/",
        "e_code" : 200,
        "e_string" : "Historia wpisów",
        "m_string" : "Wybrany użytkownik nie istnieje.",
        "m_code" : 200,
        "known" : ["admin", "Lesik"],
        "cat" : "social"
       },
       {
        "name" : "Polarsteps",
        "uri_check" : "https://api.polarsteps.com/users/byusername/{account}",
        "uri_pretty" : "https://www.polarsteps.com/{account}",
        "e_code" : 200,
        "e_string" : "\"id\":",
        "m_string" : "<title>404 Not Found</title>",
        "m_code" : 404,
        "known" : ["EngelBos", "GunnarEndlich"],
        "cat" : "hobby"
       },
       {
        "name" : "policja2009",
        "uri_check" : "http://www.policja2009.fora.pl/search.php?search_author={account}",
        "e_code" : 200,
        "e_string" : "Autor",
        "m_string" : "Nie znaleziono tematów ani postów pasujących do Twoich kryteriów",
        "m_code" : 200,
        "known" : ["Pvwel", "janek"],
        "cat" : "misc"
       },
       {
        "name" : "Poll Everywhere",
        "uri_check" : "https://pollev.com/proxy/api/users/{account}",
        "uri_pretty" : "https://pollev.com/{account}",
        "e_code" : 200,
        "e_string" : "name",
        "m_string" : "ResourceNotFound",
        "m_code" : 404,
        "known" : ["josh", "jsmith"],
        "cat" : "tech"
       },
       {
        "name" : "Mastodon-pol.social",
        "uri_check" : "https://pol.social/@{account}",
        "e_code" : 200,
        "e_string" : "@pol.social",
        "m_string" : "The page you are looking for isn't here.",
        "m_code" : 404,
        "known" : ["ftdl", "ducensor"],
        "cat" : "social"
       },
       {
        "name" : "Poe.com",
        "uri_check" : "https://poe.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "\"__isNode\":\"PoeUser\"",
        "m_code" : 200,
        "m_string" : "\"user\":null",
        "known" : ["spdustin", "PromptCase"],
        "cat" : "tech"
       },
       {
        "name" : "polygon",
        "uri_check" : "https://www.polygon.com/users/{account}",
        "e_code" : 200,
        "e_string" : "- Polygon",
        "m_string" : "404 Not found",
        "m_code" : 404,
        "known" : ["nicodeyo", "Nicole_Clark"],
        "cat" : "gaming"
       },
       {
        "name" : "popl",
        "uri_check" : "https://poplme.co/{account}",
        "e_code" : 200,
        "e_string" : "MuiTypography-root MuiTypography-body1 css-kj7pvm",
        "m_string" : "Profile not found",
        "m_code" : 200,
        "known" : ["rpelite","Ee0af3d822","ashleymetzger"],
        "cat" : "business"
       },
       {
        "name" : "Pornhub Porn Stars",
        "uri_check" : "https://www.pornhub.com/pornstar/{account}",
        "e_code" : 200,
        "e_string" : "Pornstar Rank",
        "m_string" : "",
        "m_code" : 301,
        "known" : ["riley-reid", "alex-adams"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "Pornhub Users",
        "uri_check" : "https://www.pornhub.com/users/{account}",
        "e_code" : 200,
        "e_string" : "s Profile - Pornhub.com</title>",
        "m_string" : "Error Page Not Found",
        "m_code" : 404,
        "known" : ["test123"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "Poshmark",
        "uri_check" : "https://poshmark.com/closet/{account}",
        "e_code" : 200,
        "e_string" : " is using Poshmark to sell items from their closet.",
        "m_string" : "Page not found - Poshmark",
        "m_code" : 404,
        "known" : ["alice", "bob"],
        "cat" : "shopping"
       },
       {
        "name" : "postcrossing",
        "uri_check" : "https://www.postcrossing.com/user/{account}",
        "e_code" : 200,
        "e_string" : ", from",
        "m_string" : "- Postcrossing",
        "m_code" : 404,
        "known" : ["Vladimir", "olga3"],
        "cat" : "social"
       },
       {
        "name" : "Poweredbygay.social (Mastodon Instance)",
        "uri_check" : "https://poweredbygay.social/api/v1/accounts/lookup?acct={account}",
        "uri_pretty" : "https://poweredbygay.social/@{account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_code" : 404,
        "m_string" : "Record not found",
        "known" : ["aggiepm", "eplumley1976"],
        "cat" : "social"
       },
       {
        "name" : "Pravda.me",
        "uri_check" : "https://pravda.me/@{account}",
        "e_code" : 200,
        "e_string" : "Российская социальная сеть (by mastodon)</title>",
        "m_string" : "<title>The page you are looking for isn&#39;t here.",
        "m_code" : 404,
        "known" : ["tass", "rt_russian"],
        "cat" : "social"
       },
       {
        "name" : "Privacy Guides",
        "uri_check" : "https://discuss.privacyguides.net/u/{account}.json",
        "uri_pretty" : "https://discuss.privacyguides.net/u/{account}/summary",
        "e_code" : 200,
        "e_string" : "assign_path",
        "m_string" : "The requested URL or resource could not be found.",
        "m_code" : 404,
        "known" : ["jonah", "dngray"],
        "cat" : "tech"
       },
       {
        "name" : "Producthunt",
        "uri_check" : "https://www.producthunt.com/@{account}",
        "e_code" : 200,
        "e_string" : "s profile on Product Hunt",
        "m_string" : "Product Hunt - All newest Products",
        "m_code" : 404,
        "known" : ["alex", "jack"],
        "cat" : "business"
       },
       {
        "name" : "promodj",
        "uri_check" : "https://promodj.com/{account}",
        "e_code" : 200,
        "e_string" : "Favorite styles",
        "m_string" : "Page not found :(",
        "m_code" : 404,
        "known" : ["john", "bob"],
        "cat" : "music"
       },
       {
        "name" : "Pronouns.Page",
        "uri_check" : "https://pronouns.page/api/profile/get/{account}?version=2",
        "uri_pretty" : "https://pronouns.page/@{account}",
        "e_code" : 200,
        "e_string" : "username",
        "m_string" : "\"profiles\": {}",
        "m_code" : 304,
        "known" : ["cannabis_cervi", "user"],
        "cat" : "social"
       },
       {
        "name" : "Pronouny",
        "uri_check" : "https://pronouny.xyz/api/users/profile/username/{account}",
        "e_code" : 200,
        "e_string" : "username",
        "m_code" : 400,
        "m_string" : "That user doesn't exist",
        "known" : ["test", "honey"],
        "cat" : "social"
       },
       {
        "name" : "Prose",
        "uri_check" : "https://prose.astral.camp/{account}/",
        "e_code" : 200,
        "e_string" : "blog-title",
        "m_code" : 404,
        "m_string" : "Are you sure it was ever here?",
        "known" : ["endeavorance", "overthinkification"],
        "cat" : "blog"
       },
       {
        "name" : "prv.pl",
        "uri_check" : "https://www.prv.pl/osoba/{account}",
        "e_code" : 200,
        "e_string" : "LOGIN",
        "m_string" : "Użytkownik nie istnieje.",
        "m_code" : 200,
        "known" : ["test", "test2"],
        "cat" : "tech"
       },
       {
        "name" : "public",
        "uri_check" : "https://public.com/@{account}",
        "e_code" : 200,
        "e_string" : ") Investment Portfolio on Public",
        "m_string" : "04 - Page Not Found - Public ",
        "m_code" : 404,
        "known" : ["igor1", "david2"],
        "cat" : "finance"
       },
       {
        "name" : "pypi",
        "uri_check" : "https://pypi.org/user/{account}/",
        "e_code" : 200,
        "e_string" : "Profile of",
        "m_string" : "Page Not Found (404) · PyPI",
        "m_code" : 404,
        "known" : ["dev", "pydude"],
        "cat" : "coding"
       },
       {
        "name" : "npm",
        "uri_check" : "https://www.npmjs.com/~{account}",
        "e_code" : 200,
        "e_string" : "/npm-avatar/",
        "m_string" : "poster depicting npm&#x27;s mascot wombat",
        "m_code" : 404,
        "known" : ["npm", "rich_harris"],
        "cat" : "coding"
       },
       {
        "name" : "QUEER PL",
        "uri_check" : "https://queer.pl/user/{account}",
        "e_code" : 200,
        "e_string" : "Ostatnio on-line",
        "m_string" : "Strona nie została znaleziona",
        "m_code" : 404,
        "known" : ["claudii", "kowalski"],
        "cat" : "social"
       },
       {
        "name" : "Quizlet",
        "uri_check" : "https://quizlet.com/webapi/3.2/users/check-username?username={account}",
        "uri_pretty" : "https://quizlet.com/user/{account}/sets",
        "e_code" : 200,
        "e_string" : "\"success\":false",
        "m_string" : "\"success\":true",
        "m_code" : 200,
        "known" : ["Rita426", "Muyao_531"],
        "cat" : "hobby",
        "protection" : ["cloudflare"]
       },
       {
        "name" : "quitter.pl",
        "uri_check" : "https://quitter.pl/profile/{account}",
        "e_code" : 200,
        "e_string" : "@quitter.pl",
        "m_string" : "Nie znaleziono",
        "m_code" : 404,
        "known" : ["divmod", "panoptykon"],
        "cat" : "social"
       },
       {
        "name" : "Quora",
        "uri_check" : "https://www.quora.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "Credentials",
        "m_string" : "Page Not Found",
        "m_code" : 301,
        "known" : ["John-Galan-5", "Alex-Clay"],
        "cat" : "social"
       },
       {
        "name" : "Raddle.me",
        "uri_check" : "https://raddle.me/user/{account}",
        "e_code" : 200,
        "e_string" : "sidebar__title",
        "m_code" : 404,
        "m_string" : "404 Not Found",
        "known" : ["zephyr", "Archaplain"],
        "cat" : "social"
       },
       {
        "name" : "Rarible",
        "uri_check" : "https://rarible.com/marketplace/api/v4/urls/{account}",
        "uri_pretty" : "https://rarible.com/{account}",
        "e_code" : 200,
        "e_string" : "\"id\":",
        "m_string" : "\"success\":false",
        "m_code" : 404,
        "known" : ["lokikot", "vintagemozart"],
        "cat" : "tech"
       },
       {
        "name" : "Rant.li",
        "uri_check" : "https://rant.li/{account}/",
        "e_code" : 200,
        "e_string" : "blog-title",
        "m_code" : 404,
        "m_string" : "Are you sure it was ever here?",
        "known" : ["baretri", "arinbasu"],
        "cat" : "blog"
       },
       {
        "name" : "ReblogMe",
        "uri_check" : "https://{account}.reblogme.com",
        "in_chars" : ".",
        "e_code" : 200,
        "e_string" : "blogbody",
        "m_string" : "Sorry, seems that blog doesn't exist",
        "m_code" : 200,
        "known" : ["staff", "chicken"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "Refsheet",
        "uri_check" : "https://refsheet.net/{account}",
        "e_code" : 200,
        "e_string" : "og:title",
        "m_code" : 404,
        "m_string" : "That's unfortunate. Where did it go?",
        "known" : ["razzyaurealis", "saki"],
        "cat" : "hobby"
       },
       {
        "name" : "redbubble",
        "uri_check" : "https://www.redbubble.com/people/{account}/shop",
        "e_code" : 200,
        "e_string" : "Shop | Redbubble",
        "m_string" : "This is a lost cause.",
        "m_code" : 404,
        "known" : ["john", "blue"],
        "cat" : "shopping"
       },
       {
        "name" : "Reddit",
        "uri_check" : "https://www.reddit.com/user/{account}/about/.json",
        "uri_pretty" : "https://www.reddit.com/user/{account}",
        "e_code" : 200,
        "e_string" : "total_karma",
        "m_string" : "Not Found",
        "m_code" : 404,
        "known" : ["koavf", "alabasterheart"],
        "cat" : "social"
       },
       {
        "name" : "REDGIFS",
        "uri_check" : "https://api.redgifs.com/v1/users/{account}",
        "uri_pretty" : "https://www.redgifs.com/users/{account}",
        "e_code" : 200,
        "e_string" : "followers",
        "m_string" : "user account not found for ",
        "m_code" : 404,
        "known" : ["alexbreecooper", "Jose-Roberto-Rasi"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "Replit web",
        "uri_check" : "https://replit.com/@{account}",
        "e_code" : 200,
        "e_string" : "Copy profile link",
        "m_code" : 404,
        "m_string" : "<title>Replit - 404 - Replit</title>",
        "known" : ["david", "torcado"],
        "cat" : "coding"
       },
       {
        "name" : "Replit cli",
        "uri_check" : "https://replit.com/@{account}",
        "e_code" : 200,
        "e_string" : "Copy profile link",
        "m_code" : 404,
        "m_string" : "User not found",
        "known" : ["david", "torcado"],
        "cat" : "coding"
       },
       {
        "name" : "Researchgate",
        "uri_check" : "https://www.researchgate.net/profile/{account}",
        "e_code" : 200,
        "e_string" : " | ",
        "m_string" : "20+ million researchers on ResearchGate",
        "m_code" : 301,
        "known" : ["Tafara-Mwareya", "Jose-Roberto-Rasi"],
        "cat" : "hobby"
       },
       {
        "name" : "resumes_actorsaccess",
        "uri_check" : "https://resumes.actorsaccess.com/{account}",
        "e_code" : 200,
        "e_string" : "- Resume | Actors Access</title>",
        "m_string" : "File was not found on this SERVER",
        "m_code" : 200,
        "known" : ["veronicashelby", "sarahstipe"],
        "cat" : "social"
       },
       {
        "name" : "Revolut",
        "uri_check" : "https://revolut.me/api/web-profile/{account}",
        "uri_pretty" : "https://revolut.me/{account}",
        "e_code" : 200,
        "e_string" : "\"firstName\"",
        "m_code" : 404,
        "m_string" : "\"User not found\"",
        "known" : ["theaswdc", "honey"],
        "cat" : "finance"
       },
       {
        "name" : "Mastodon-rigcz.club",
        "uri_check" : "https://rigcz.club/@{account}",
        "e_code" : 200,
        "e_string" : "@rigcz.club",
        "m_string" : "The page you are looking for isn't here.",
        "m_code" : 404,
        "known" : ["blazej", "adam"],
        "cat" : "social"
       },
       {
        "name" : "RblxTrade",
        "uri_check" : "https://rblx.trade/api/v1/user/get-by-username?username={account}",
        "uri_pretty" : "https://rblx.trade/p/{account}",
        "e_code" : 200,
        "e_string" : "\"userId\":",
        "m_string" : "\"success\":false",
        "m_code" : 400,
        "known" : ["webbreacher", "SonOfSevenless"],
        "cat" : "gaming"
       },
       {
        "name" : "risk.ru",
        "uri_check" : "https://risk.ru/people/{account}",
        "e_code" : 200,
        "e_string" : "— Люди — Risk.ru",
        "m_string" : "404 — Risk.ru",
        "m_code" : 404,
        "known" : ["igor1", "olga"],
        "cat" : "hobby"
       },
       {
        "name" : "Roblox",
        "uri_check" : "https://auth.roblox.com/v1/usernames/validate?username={account}&birthday=2019-12-31T23:00:00.000Z",
        "uri_pretty" : "https://www.roblox.com/search/users?keyword={account}",
        "e_code" : 200,
        "e_string" : "Username is already in use",
        "m_string" : "Username is valid",
        "m_code" : 200,
        "known" : ["LeetPawn", "elephant459"],
        "cat" : "gaming"
       },
       {
        "name" : "RoutineHub",
        "uri_check" : "https://routinehub.co/user/{account}",
        "e_code" : 200,
        "e_string" : "Downloads: ",
        "m_string" : "A community for Apple Shortcuts</title>",
        "m_code" : 200,
        "known" : ["zachary7829", "JonathanSetzer"],
        "cat" : "social"
       },
       {
        "name" : "rsi",
        "uri_check" : "https://robertsspaceindustries.com/citizens/{account}",
        "e_code" : 200,
        "e_string" : "CITIZEN DOSSIER",
        "m_string" : "404 NAVIGATING UNCHARTED TERRITORY",
        "m_code" : 404,
        "known" : ["alpHackeronee", "Quantum_Physicist"],
        "cat" : "gaming"
       },
       {
        "name" : "RuTracker.org",
        "uri_check" : "https://rutracker.org/forum/profile.php?mode=viewprofile&u={account}",
        "e_code" : 200,
        "e_string" : "Профиль пользователя",
        "m_string" : "Пользователь не найден",
        "m_code" : 200,
        "known" : ["Rutracker", "Feo156"],
        "cat" : "misc"
       },
       {
        "name" : "ru_123rf",
        "uri_check" : "https://ru.123rf.com/profile_{account}",
        "e_code" : 200,
        "e_string" : "userID",
        "m_string" : "<title>Фотобанк 123RF - Стоковые Фото, Векторы, Видеоролики. Подписка на Фото. Royalty Free контент<",
        "m_code" : 302,
        "known" : ["ruslan", "olga"],
        "cat" : "hobby"
       },
       {
        "name" : "RumbleChannel",
        "uri_check" : "https://rumble.com/c/{account}",
        "e_code" : 200,
        "e_string" : "href=https://rumble.com/c/",
        "m_string" : "404 error, this page does not exist",
        "m_code" : 404,
        "known" : ["SaltyCracker", "GGreenwald"],
        "cat" : "political"
       },
       {
        "name" : "RumbleUser",
        "uri_check" : "https://rumble.com/user/{account}",
        "e_code" : 200,
        "e_string" : "href=https://rumble.com/user/",
        "m_string" : "404 error, this page does not exist",
        "m_code" : 404,
        "known" : ["SimonParkes", "djmrmusic"],
        "cat" : "political"
       },
       {
        "name" : "Salon24",
        "uri_check" : "https://www.salon24.pl/u/{account}/",
        "e_code" : 200,
        "e_string" : "<span>Obserwujących</span>",
        "m_string" : "<title>Salon24 - Blogi, wiadomości, opinie i komentarze",
        "m_code" : 301,
        "known" : ["matuzalem", "niewiarygodne"],
        "cat" : "blog"
       },
       {
        "name" : "ScoutWiki",
        "uri_check" : "https://en.scoutwiki.org/User:{account}",
        "e_code" : 200,
        "e_string" : "NewPP limit report",
        "m_string" : "is not registered",
        "m_code" : 301,
        "known" : ["Mlh_nl", "Benjism89"],
        "cat" : "social"
       },
       {
        "name" : "scratch",
        "uri_check" : "https://scratch.mit.edu/users/{account}/",
        "e_code" : 200,
        "e_string" : "on Scratch</title>",
        "m_string" : "We couldn't find the page you're looking for.",
        "m_code" : 404,
        "known" : ["griffpatch"],
        "cat" : "coding"
       },
       {
        "name" : "secure_donation",
        "uri_check" : "https://secure.donationpay.org/{account}/",
        "e_code" : 200,
        "e_string" : "| DonationPay</title>",
        "m_string" : "<title>secure.donationpay.org</title>",
        "m_code" : 404,
        "known" : ["rareimpact", "safc"],
        "cat" : "finance"
       },
       {
        "name" : "sedisp@ce",
        "uri_check" : "https://sedispace.com/@{account}",
        "e_code" : 200,
        "e_string" : "Membre depuis -",
        "m_string" : "- Page non trouvée!",
        "m_code" : 302,
        "known" : ["mamadou", "konate"],
        "cat" : "social"
       },
       {
        "name" : "Seneporno",
        "uri_check" : "https://seneporno.com/user/{account}",
        "e_code" : 200,
        "e_string" : "Dernier Login",
        "m_string" : "Unexpected error! Please contact us and tell us more how you got to this page!",
        "m_code" : 301,
        "known" : ["Kalsobbc", "Boymariste"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "sentimente",
        "uri_check" : "https://www.sentimente.com/amp/{account}.html",
        "e_code" : 200,
        "e_string" :"Chat online with",
        "m_string" : "HTTP Error code: 404. Resource not found",
        "m_code" : 404,
        "known" : ["david01", "brahim01"],
        "cat" : "dating"
       },
       {
        "name" : "SEOClerks",
        "uri_check" : "https://www.seoclerks.com/user/{account}",
        "e_code" : 200,
        "e_string" : "<div class=\"user-info container\">",
        "m_string" : "<title>SEO Marketplace",
        "m_code" : 302,
        "known" : ["Vfmseo", "gokudadon"],
        "cat" : "social"
       },
       {
        "name" : "setlist.fm",
        "uri_check" : "https://www.setlist.fm/user/{account}",
        "e_code" : 200,
        "e_string" : "s setlist.fm | setlist.fm</title>",
        "m_string" : "Sorry, the page you requested doesn't exist",
        "m_code" : 404,
        "known" : ["bendobrin", "michi"],
        "cat" : "music"
       },
       {
        "name" : "Sexworker",
        "uri_check" : "https://sexworker.com/api/profile/{account}",
        "uri_pretty" : "https://sexworker.com/{account}",
        "e_code" : 200,
        "e_string" : "profilePictureUrl",
        "m_code" : 404,
        "m_string" : "This user does not exist.",
        "known" : ["sakii_nightshade", "annajean2319"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "SFD",
        "uri_check" : "https://www.sfd.pl/profile/{account}",
        "e_code" : 200,
        "e_string" : "Tematy użytkownika",
        "m_string" : "Brak aktywnego profilu na forum",
        "m_code" : 404,
        "known" : ["janek", "admin"],
        "cat" : "health"
       },
       {
        "name" : "Shesfreaky",
        "uri_check" : "https://www.shesfreaky.com/profile/{account}/",
        "e_code" : 200,
        "e_string" : "s Profile - ShesFreaky</title>",
        "m_code" : 302,
        "m_string" : "",
        "known" : ["tata23", "fitzsta"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "shopify",
        "uri_check" : "https://{account}.myshopify.com",
        "strip_bad_char" : ".",
        "e_code" : 200,
        "e_string" : "home",
        "m_string" : "Sorry, this shop is currently unavailable.",
        "m_code" : 404,
        "known" : ["john", "daniel"],
        "cat" : "shopping"
       },
       {
        "name" : "Showup.tv",
        "uri_check" : "https://showup.tv/profile/{account}",
        "e_code" : 200,
        "e_string" : "O mnie",
        "m_string" : "<title>Darmowe",
        "m_code" : 404,
        "known" : ["LunaVee", "Jane_Frou"],
        "cat" : "xx NSFW xx",
        "headers" : {
          "Cookie" : "accept_rules=true;"
        }
       },
       {
        "name" : "shutterstock",
        "uri_check" : "https://www.shutterstock.com/g/{account}",
        "e_code" : 200,
        "e_string" : "| Shutterstock",
        "m_string" : "Well, this is unexpected...",
        "m_code" : 404,
        "known" : ["john", "bob"],
        "cat" : "images"
       },
       {
        "name" : "SimplePlanes",
        "uri_check" : "https://www.simpleplanes.com/u/{account}",
        "e_code" : 200,
        "e_string" : "<h5>joined",
        "m_code" : 302,
        "m_string" : "<title>SimplePlanes Airplanes</title>",
        "known" : ["realSavageMan", "Jundroo", "john"],
        "cat" : "gaming"
       },
       {
        "name" : "skeb",
        "uri_check" : "https://skeb.jp/@{account}",
        "e_code" : 200,
        "e_string" : ") | Skeb",
        "m_code" : 503,
        "m_string" : "Skeb - Request Box",
        "known" : ["eipuru_", "sime064"],
        "cat" : "art"
       },
       {
        "name" : "SlackHoles",
        "uri_check" : "https://slackholes.com/actor/{account}/",
        "e_code" : 200,
        "e_string" : "Pussy and Ass Sizes",
        "m_string" : "It looks like nothing was found at this location",
        "m_code" : 404,
        "known" : ["alexbreecooper", "roxy-raye"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "slant",
        "uri_check" : "https://www.slant.co/users/{account}",
        "e_code" : 200,
        "e_string" : "s Profile - Slant",
        "m_string" : "404 - Page Not Found - Slant",
        "m_code" : 404,
        "known" : ["bob", "john"],
        "cat" : "shopping"
       },
       {
        "name" : "slideshare",
        "uri_check" : "https://www.slideshare.net/{account}",
        "e_code" : 200,
        "e_string" : "photo user-photo",
        "m_string" : "is still available. Why not",
        "m_code" : 404,
        "known" : ["test"],
        "cat" : "social"
       },
       {
        "name" : "slides",
        "uri_check" : "https://slides.com/{account}",
        "e_code" : 200,
        "e_string" : "Presentations by",
        "m_string" : "You may have mistyped the address",
        "m_code" : 404,
        "known" : ["arunthomas"],
        "cat" : "social"
       },
       {
        "name" : "SmashRun",
        "uri_check" : "https://smashrun.com/{account}/",
        "e_code" : 200,
        "e_string" : "Miles run overall",
        "m_string" : "no Smashrunner with the username",
        "m_code" : 404,
        "known" : ["john.young"],
        "cat" : "health"
       },
       {
        "name" : "smelsy",
        "uri_check" : "https://www.smelsy.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "Smelsy -",
        "m_string" : "Server Error",
        "m_code" : 500,
        "known" : ["mohamed01", "ahmed"],
        "cat" : "misc"
       },
       {
        "name" : "SmugMug",
        "uri_check" : "https://{account}.smugmug.com",
        "strip_bad_char" : ".",
        "e_code" : 200,
        "e_string" : "schema.org/Person",
        "m_string" : "schema.org/Thing",
        "m_code" : 404,
        "known" : ["wow", "jill"],
        "cat" : "images"
       },
       {
        "name" : "smule",
        "uri_check" : "https://www.smule.com/api/profile/?handle={account}",
        "uri_pretty" : "https://www.smule.com/{account}",
        "e_code" : 200,
        "e_string" : "account_id",
        "m_string" : "code\": 65",
        "m_code" : 400,
        "known" : ["cgrrose", "John___Anish"],
        "cat" : "music"
       },
       {
        "name" : "Snapchat",
        "uri_check" : "https://www.snapchat.com/add/{account}",
        "e_code" : 200,
        "e_string" : "is on Snapchat!",
        "m_string" : "NOT_FOUND",
        "m_code" : 200,
        "known" : ["djkhaled305", "mileycyrus"],
        "cat" : "social"
       },
       {
        "name" : "Snipfeed",
        "uri_check" : "https://snipfeed.co/{account}",
        "e_code" : 200,
        "e_string" : "creatorLink",
        "m_code" : 404,
        "m_string" : "Oops, you hit a dead end!",
        "known" : ["mycherrycrush", "honey"],
        "cat" : "misc"
       },
       {
        "name" : "social.bund.de",
        "uri_check" : "https://social.bund.de/@{account}",
        "e_code" : 200,
        "e_string" : "@social.bund.de) - social.bund.de</title>",
        "m_string" : "<title>The page you are looking for isn&#39;t here.",
        "m_code" : 404,
        "known" : ["bfdi", "bmdv"],
        "cat" : "social"
       },
       {
        "name" : "soc.citizen4.eu",
        "uri_check" : "https://soc.citizen4.eu/profile/{account}/profile",
        "e_code" : 200,
        "e_string" : "@soc.citizen4.eu",
        "m_string" : "Nie znaleziono",
        "m_code" : 404,
        "known" : ["admin", "miklo"],
        "cat" : "social"
       },
       {
        "name" : "social_msdn",
        "uri_check" : "https://social.msdn.microsoft.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "Member Since",
        "m_string" : "The resource you are looking for has been removed, had its name changed, or is temporarily unavailable.",
        "m_code" : 404,
        "known" : ["edoardo", "microsoftfan"],
        "cat" : "social"
       },
       {
        "name" : "Mastodon-social_tchncs",
        "uri_check" : "https://social.tchncs.de/@{account}",
        "e_code" : 200,
        "e_string" : "profile:username",
        "m_string" : "The page you are looking for isn&#39;t here",
        "m_code" : 301,
        "known" : ["michael", "frank"],
        "cat" : "social"
       },
       {
        "name" : "sofurry",
        "uri_check" : "https://{account}.sofurry.com",
        "strip_bad_char" : ".",
        "e_code" : 200,
        "e_string" : "'s Profile | SoFurry",
        "m_string" : "SoFurry - Error | SoFurry",
        "m_code" : 404,
        "known" : ["reeden-landshey", "tigerzero"],
        "cat" : "art"
       },
       {
        "name" : "solo.to",
        "uri_check" : "https://solo.to/{account}",
        "e_code" : 200,
        "e_string" : "create your own page",
        "m_code" : 404,
        "m_string" : "The page you're looking for isn't here.",
        "known" : ["saruei", "yui"],
        "cat" : "social"
       },
       {
        "name" : "SoundCloud",
        "uri_check" : "https://soundcloud.com/{account}",
        "e_code" : 200,
        "e_string" : "SoundCloud</title>",
        "m_string" : "sounds</title>",
        "m_code" : 404,
        "known" : ["test123"],
        "cat" : "music"
       },
       {
        "name" : "Soup",
        "uri_check" : "https://www.soup.io/author/{account}",
        "e_code" : 200,
        "e_string" : "Author at Soup.io",
        "m_string" : "Soup.io - News, Sports, Entertainment, TV, Tech, Gaming",
        "m_code" : 301,
        "known" : ["john", "cristina"],
        "cat" : "blog"
       },
       {
        "name" : "Sourceforge",
        "uri_check" : "https://sourceforge.net/user/username/{account}",
        "uri_pretty" : "https://sourceforge.net/u/{account}/profile",
        "e_code" : 400,
        "e_string" : "\"error\": \"invalid\"",
        "m_string" : "\"success\": 1",
        "m_code" : 200,
        "known" : ["alice", "bob"],
        "cat" : "coding",
        "protection": ["cloudflare"]
       },
       {
        "name" : "Speaker Deck",
        "uri_check" : "https://speakerdeck.com/{account}/",
        "e_code" : 200,
        "e_string" : ") on Speaker Deck</title>",
        "m_string" : "User Not Found - Speaker Deck",
        "m_code" : 404,
        "known" : ["petecheslock", "turbosmart45"],
        "cat" : "social"
       },
       {
        "name" : "speedrun",
        "uri_check" : "https://www.speedrun.com/user/{account}/",
        "e_code" : 200,
        "e_string" : "Runs - ",
        "m_string" : "<title>speedrun.com",
        "m_code" : 404,
        "known" : ["mike", "chris"],
        "cat" : "gaming"
       },
       {
        "name" : "SpiceWorks",
        "uri_check" : "https://community.spiceworks.com/people/{account}",
        "e_code" : 200,
        "e_string" : "Portfolio of IT Projects - Spiceworks",
        "m_string" : "Page Not Found",
        "m_code" : 404,
        "known" : ["spicerex", "rod-it"],
        "cat" : "tech"
       },
      {
        "name" : "SPOJ",
        "uri_check" : "https://www.spoj.com/users/{account}/",
        "e_code" : 200,
        "e_string" : "<h3>Activity over the last year</h3>",
        "m_string" : "<strong>Innopolis Open 2018</strong>",
        "m_code" : 200,
        "known" : ["defrager", "xilinx"],
        "cat" : "coding"
       },
       {
        "name" : "sporcle",
        "uri_check" : "https://www.sporcle.com/user/{account}/people/",
        "e_code" : 200,
        "e_string" : "'s Sporcle Friends",
        "m_string" : "This Sporcle user cannot be found.",
        "m_code" : 301,
        "known" : ["Test", "lolshortee"],
        "cat" : "gaming"
       },
       {
        "name" : "Spotify",
        "uri_check" : "https://open.spotify.com/user/{account}",
        "e_code" : 200,
        "e_string" : "content=\"profile\"",
        "m_string" : "Page not found",
        "m_code" : 404,
        "known" : ["kexp_official", "mkbhd"],
        "cat" : "music",
        "protection" : ["other"]
       },
       {
        "name" : "StackOverflow",
        "uri_check" : "https://stackoverflow.com/users/filter?search={account}",
        "e_code" : 200,
        "e_string" : "grid--item user-info",
        "m_string" : "No users matched your search.",
        "m_code" : 200,
        "known" : ["vonc", "bergi"],
        "cat" : "coding",
        "protection" : ["cloudflare"]
       },
       {
        "name" : "Steam",
        "uri_check" : "https://steamcommunity.com/id/{account}",
        "e_code" : 200,
        "e_string" : "g_rgProfileData =",
        "m_string" : "Steam Community :: Error",
        "m_code" : 200,
        "known" : ["test"],
        "cat" : "gaming"
       },
       {
        "name" : "SteamGifts",
        "uri_check" : "https://www.steamgifts.com/user/{account}",
        "e_code" : 200,
        "e_string" : "\"identifier\":",
        "m_string" : "",
        "m_code" : 301,
        "known" : ["AbsurdPoncho", "Wolod1402"],
        "cat" : "gaming"
       },
       {
        "name" : "Steemit",
        "uri_check"  : "https://signup.steemit.com/api/check_username",
        "uri_pretty" : "https://steemit.com/@{account}",
        "post_body" : "{\"username\":\"{account}\"}",
        "e_code" : 200,
        "e_string" : "\"type\":\"error_api_username_used\"",
        "m_string" : "\"success\":true",
        "m_code" : 200,
        "known" : ["petlover", "zalat"],
        "cat" : "social",
        "headers" : {
            "Content-Type" : "application/json"
        }
       },
       {
        "name" : "steller",
        "uri_check" : "https://steller.co/{account}",
        "e_code" : 200,
        "e_string" : " on Steller</title>",
        "m_string" : "<title></title>",
        "m_code" : 404,
        "known" : ["jeannnn", "havwoods"],
        "cat" : "shopping"
       },
       {
        "name" : "Statuspage",
        "uri_check" : "https://{account}.statuspage.io/api/v2/status.json",
        "uri_pretty" : "https://{account}.statuspage.io/",
        "e_code" : 200,
        "e_string" : "updated_at",
        "m_string" : "<html><body>You are being <a href=\"https://www.statuspage.io\">redirected</a>.</body></html>",
        "m_code" : 302,
        "known" : ["8713981tpdlg", "gaming", "coinbase"],
        "cat" : "tech"
       },
       {
        "name" : "StoryCorps",
        "uri_check" : "https://archive.storycorps.org/user/{account}/",
        "e_code" : 200,
        "e_string" : "archive author",
        "m_string" : "We're sorry, but the page",
        "m_code" : 404,
        "known" : ["jthorstad", "paul-swider"],
        "cat" : "blog"
       },
       {
        "name" : "StreamElements",
        "uri_check" : "https://api.streamelements.com/kappa/v2/channels/{account}",
        "uri_pretty" : "https://streamelements.com/{account}",
        "e_code" : 200,
        "e_string" : "\"providerId\"",
        "m_code" : 404,
        "m_string" : "error",
        "known" : ["honey", "dude"],
        "cat" : "finance"
       },
       {
        "name" : "StreamLabs",
        "uri_check" : "https://streamlabs.com/api/v6/user/{account}",
        "uri_pretty" : "https://streamlabs.com/{account}/tip",
        "e_code" : 200,
        "e_string" : "\"id\":",
        "m_code" : 401,
        "m_string" : "<title>Unauthorized</title>",
        "known" : ["veibae", "cutie_cori"],
        "cat" : "finance"
       },
       {
        "name" : "Stripchat",
        "uri_check" : "https://stripchat.com/api/front/users/checkUsername?username={account}",
        "uri_pretty" : "https://stripchat.com/{account}",
        "e_code" : 400,
        "e_string" : "\"error\":",
        "m_string" : "[]",
        "m_code" : 200,
        "known" : ["DulcieRichard", "Katie-Mili"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "Subscribestar",
        "uri_check" : "https://subscribestar.adult/{account}",
        "e_code" : 200,
        "e_string" : "CREATOR STATS",
        "m_code" : 404,
        "m_string" : "WE ARE SORRY, THE PAGE YOU REQUESTED CANNOT BE FOUND",
        "known" : ["missmoonified", "honey"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "Substack",
        "uri_check" : "https://substack.com/@{account}",
        "e_code" : 200,
        "e_string" : "| Substack</title>",
        "m_code" : 200,
        "m_string" : "&quot; on Substack</title>",
        "known" : ["janellehardacre", "janeclairebradley"],
        "cat" : "social"
       },
       {
        "name" : "sukebei.nyaa.si",
        "uri_check" : "https://sukebei.nyaa.si/user/{account}",
        "e_code" : 200,
        "e_string" : "'s torrents",
        "m_code" : 404,
        "m_string" : "404 Not Found",
        "known" : ["kouhy76", "Rektr0"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "Suzuri",
        "uri_check" : "https://suzuri.jp/{account}",
        "e_code" : 200,
        "e_string" : "Items",
        "m_string" : "Push Space-key",
        "m_code" : 404,
        "known" : ["itochanxxx", "alex"],
        "cat" : "business"
       },
       {
        "name" : "szmer.info",
        "uri_check" : "https://szmer.info/u/{account}",
        "e_code" : 200,
        "e_string" : "Joined",
        "m_string" : "Code: Couldn't find that username or email.",
        "m_code" : 200,
        "known" : ["przeczzpreczem", "Xavier"],
        "cat" : "social"
       },
       {
        "name" : "tabletoptournament",
        "uri_check" : "https://www.tabletoptournaments.net/eu/player/{account}",
        "e_code" : 200,
        "e_string" : "- Player Profile | T³ - TableTop Tournaments",
        "m_string" : "No player with the nickname",
        "m_code" : 200,
        "known" : ["Lars01", "john"],
        "cat" : "misc"
       },
       {
        "name" : "Tagged",
        "uri_check" : "https://secure.tagged.com/{account}",
        "e_code" : 200,
        "e_string" : "s Profile</title>",
        "m_string" : "Tagged - The social network for meeting new people",
        "m_code" : 302,
        "known" : ["Samantha", "Robert"],
        "cat" : "social"
       },
       {
        "name" : "TamTam",
        "uri_check" : "https://tamtam.chat/{account}",
        "e_code" : 200,
        "e_string" : "deeplink=tamtam://chat/",
        "m_string" : "ТамТам</title>",
        "m_code" : 302,
        "known" : ["blue", "John"],
        "cat" : "social"
       },
       {
        "name" : "Tanuki.pl",
        "uri_check" : "https://tanuki.pl/profil/{account}",
        "e_code" : 200,
        "e_string" : "Dołączył",
        "m_string" : "Nie ma takiego użytkownika",
        "m_code" : 404,
        "known" : ["ania", "avellana"],
        "cat" : "hobby"
       },
       {
        "name" : "TAPiTAG",
        "uri_check" : "https://account.tapitag.co/tapitag/api/v1/{account}",
        "uri_pretty" : "https://account.tapitag.co/{account}",
        "e_code" : 200,
        "e_string" : "User details are Showing",
        "m_string" : "The rf number is not valid",
        "m_code" : 200,
        "known" : ["JonathanWallace", "gearoidconsidine"],
        "cat" : "business"
       },
       {
        "name" : "Tappy",
        "uri_check" : "https://api.tappy.tech/api/profile/username/{account}",
        "uri_pretty" : "https://www.tappy.tech/{account}",
        "e_code" : 200,
        "e_string" : "user_id",
        "m_string" : "Profile of username Not Found",
        "m_code" : 200,
        "known" : ["alexborrelli", "domocann"],
        "cat" : "business"
       },
       {
        "name" : "Taringa",
        "uri_check" : "https://www.taringa.net/{account}",
        "e_code" : 200,
        "e_string" : " en Taringa!</title>",
        "m_string" : "Colectiva en Taringa!</title>",
        "m_code" : 301,
        "known" : ["jocaxav", "engendrometal"],
        "cat" : "social"
       },
       {
        "name" : "Taringa Archived Profile",
        "uri_check" : "https://archive.org/wayback/available?url=https://www.taringa.net/{account}",
        "uri_pretty" : "https://web.archive.org/web/2/taringa.net/{account}",
        "e_code" : 200,
        "e_string" : "\"archived_snapshots\": {\"closest\"",
        "m_string" : "\"archived_snapshots\": {}",
        "m_code" : 200,
        "known" : ["farantic", "elrubius"],
        "cat" : "archived"
       },
       {
        "name" : "taskrabbit",
        "uri_check" : "https://www.taskrabbit.com/profile/{account}/about",
        "e_code" : 200,
        "e_string" : "’s Profile",
        "m_string" : "",
        "m_code" : 302,
        "known" : ["john", "sam"],
        "cat" : "business"
       },
       {
        "name" : "TETR.IO",
        "uri_check" : "https://ch.tetr.io/api/users/{account}",
        "uri_pretty" : "https://ch.tetr.io/u/{account}",
        "e_code" : 200,
        "e_string" : "\"success\":true",
        "m_string" : "\"success\":false",
        "m_code" : 404,
        "known" : ["icly", "5han"],
        "cat" : "gaming"
       },
       {
        "name" : "Teamtreehouse",
        "uri_check" : "https://teamtreehouse.com/{account}",
        "e_code" : 200,
        "e_string" : "Member Since",
        "m_string" : "Oops, Something went missing",
        "m_code" : 404,
        "known" : ["john"],
        "cat" : "coding"
       },
       {
        "name" : "Teddygirls",
        "uri_check" : "https://teddysgirls.net/models/{account}",
        "e_code" : 200,
        "e_string" : ";s exclusive page to subscribe to her",
        "m_string" : "The page you were looking for doesn't exist",
        "m_code" : 404,
        "known" : ["jaycee-starr", "chubbychick94"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "Teespring",
        "uri_check" : "https://commerce.teespring.com/v1/stores?slug={account}",
        "uri_pretty" : "https://{account}.creator-spring.com",
        "e_code" : 200,
        "e_string" : "sellerToken",
        "m_code" : 404,
        "m_string" : "{\"errors\":{\"store\":[\"not found\"]}}",
        "known" : ["missmoonified", "honey"],
        "cat" : "business"
       },
       {
        "name" : "Teknik",
        "uri_check" : "https://user.teknik.io/{account}",
        "e_code" : 200,
        "e_string" : "Public Key",
        "m_string" : "The user does not exist",
        "m_code" : 200,
        "known" : ["red", "bob"],
        "cat" : "tech"
       },
       {
        "name" : "Telegram",
        "uri_check" : "https://t.me/{account}",
        "e_code" : 200,
        "e_string" : "tgme_page_title",
        "m_string" : "noindex, nofollow",
        "m_code" : 200,
        "known" : ["alice", "giovanni"],
        "cat" : "social"
       },
       {
        "name" : "Tellonym",
        "uri_check" : "https://tellonym.me/{account}",
        "e_code" : 200,
        "e_string" : "on Tellonym",
        "m_string" : "- Honest & Anonymous Feedback",
        "m_code" : 404,
        "known" : ["jane", "jimmy"],
        "cat" : "social"
       },
       {
        "name" : "Tenor",
        "uri_check" : "https://tenor.com/users/{account}",
        "e_code" : 200,
        "e_string" : "<div class=\"tagline\">",
        "m_code" : 404,
        "m_string" : "We could not find the page you were looking for.",
        "known" : ["gnutv", "d33jay23"],
        "cat" : "images"
       },
       {
        "name" : "TF2 Backpack Examiner",
        "uri_check" : "http://www.tf2items.com/id/{account}/",
        "e_code" : 200,
        "e_string" : "<title>TF2 Backpack -",
        "m_string" : "",
        "m_code" : 302,
        "known" : ["test"],
        "cat" : "gaming"
       },
       {
        "name" : "themeforest",
        "uri_check" : "https://themeforest.net/user/{account}",
        "e_code" : 200,
        "e_string" : "s profile on ThemeForest",
        "m_string" : "Page Not Found | ThemeForest",
        "m_code" : 301,
        "known" : ["john", "bob"],
        "cat" : "art"
       },
       {
        "name" : "thegatewaypundit",
        "uri_check" : "https://www.thegatewaypundit.com/author/{account}/",
        "e_code" : 200,
        "e_string" : "summary",
        "m_string" : "Not found, error 404",
        "m_code" : 404,
        "known" : ["patti", "joehoft"],
        "cat" : "political"
       },
       {
        "name" : "theguardian",
        "uri_check" : "https://www.theguardian.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "https://www.theguardian.com/profile/",
        "m_string" : "Page not found | The Guardian",
        "m_code" : 404,
        "known" : ["minna-salami", "johnnaughton"],
        "cat" : "news"
       },
       {
        "name" : "Thetattooforum",
        "uri_check" : "https://www.thetattooforum.com/members/{account}/",
        "e_code" : 200,
        "e_string" : "Insert This Gallery",
        "m_string" : "We’re sorry",
        "m_code" : 500,
        "known" : ["mixdop", "modifyielts"],
        "cat" : "art"
       },
       {
        "name" : "thoughts",
        "uri_check" : "https://thoughts.com/members/{account}/",
        "e_code" : 200,
        "e_string" : "<span class=\"activity",
        "m_string" : "<title>Page not found",
        "m_code" : 404,
        "known" : ["myownpersonalthoughts", "danwions"],
        "cat" : "hobby"
       },
       {
        "name" : "Threads.net",
        "uri_check" : "https://www.threads.net/@{account}",
        "e_code" : 200,
        "e_string" : ") on Threads</title>",
        "m_string" : "<title>Threads</title>",
        "m_code" : 200,
        "known" : ["s_novoselov", "oliveralexanderdk"],
        "cat" : "social"
       },
       {
        "name" : "TikTok",
        "uri_check" : "https://www.tiktok.com/oembed?url=https://www.tiktok.com/@{account}",
        "uri_pretty" : "https://www.tiktok.com/@{account}?lang=en",
        "e_code" : 200,
        "e_string" : "author_url",
        "m_string" : "Something went wrong",
        "m_code" : 400,
        "known" : ["gordonramsayofficial", "pookiebear73"],
        "cat" : "social"
       },
       {
        "name" : "Tilde.zone (Mastodon Instance)",
        "uri_check" : "https://tilde.zone/api/v1/accounts/lookup?acct={account}",
        "uri_pretty" : "https://tilde.zone/@{account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_code" : 404,
        "m_string" : "Record not found",
        "known" : ["ben", "lunatic"],
        "cat" : "social"
       },
       {
        "name" : "Tindie",
        "uri_check" : "https://www.tindie.com/accounts/check_username/",
        "uri_pretty" : "https://www.tindie.com/stores/{account}/",
        "post_body" : "username={account}",
        "e_code" : 200,
        "e_string" : "\"valid\": false",
        "m_string" : "\"valid\": true",
        "m_code" : 200,
        "known" : ["tehrabbitt", "dekunukem"],
        "cat" : "shopping",
        "headers" : {
            "Content-Type": "application/x-www-form-urlencoded"
        }
       },
       {
        "name" : "Tinder",
        "uri_check" : "https://tinder.com/@{account}",
        "e_code" : 200,
        "e_string" : ") | Tinder</title>",
        "m_string" : "Tinder | Dating, Make Friends &amp; Meet New People",
        "m_code" : 200,
        "known" : ["Alexey", "peter", "john"],
        "cat" : "dating"
       },
       {
        "name" : "Tooting.ch (Mastodon Instance)",
        "uri_check" : "https://tooting.ch/api/v1/accounts/lookup?acct={account}",
        "uri_pretty" : "https://tooting.ch/@{account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_code" : 404,
        "m_string" : "Record not found",
        "known" : ["mikebeganyi", "Zugi"],
        "cat" : "social"
       },
       {
        "name" : "TotalWar",
        "uri_check" : "https://forums.totalwar.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "Total War Forums",
        "m_string" : "Not Found",
        "m_code" : 404,
        "known" : ["iamnotarobot", "passthechips"],
        "cat" : "gaming"
       },
       {
        "name" : "toyhou.se",
        "uri_check" : "https://toyhou.se/{account}",
        "e_code" : 200,
        "e_string" : "display-user",
        "m_code" : 404,
        "m_string" : "We can't find that page!",
        "known" : ["22RII", "honey"],
        "cat" : "hobby"
       },
       {
        "name" : "tradingview",
        "uri_check" : "https://www.tradingview.com/u/{account}/",
        "e_code" : 200,
        "e_string" : "— Trading Ideas &amp;",
        "m_string" : "Page not found — TradingView",
        "m_code" : 404,
        "known" : ["liam", "john"],
        "cat" : "finance"
       },
       {
        "name" : "trakt",
        "uri_check" : "https://trakt.tv/users/{account}",
        "e_code" : 200,
        "e_string" : "s profile - Trakt",
        "m_string" : "The page you were looking for doesn't exist (404) - Trakt.tv",
        "m_code" : 404,
        "known" : ["john", "anne"],
        "cat" : "video"
       },
       {
        "name" : "Trello",
        "uri_check" : "https://trello.com/1/Members/{account}?fields=activityBlocked%2CavatarUrl%2Cbio%2CbioData%2Cconfirmed%2CfullName%2CidEnterprise%2CidMemberReferrer%2Cinitials%2CmemberType%2CnonPublic%2Cproducts%2Curl%2Cusername",
        "uri_pretty" : "https://trello.com/{account}",
        "e_code" : 200,
        "e_string" : "avatarUrl",
        "m_code" : 404,
        "m_string" : "Oh no! 404!",
        "known" : ["naranjasan", "jane"],
        "cat" : "social"
       },
       {
        "name" : "tripadvisor",
        "uri_check" : "https://www.tripadvisor.com/Profile/{account}",
        "e_code" : 200,
        "e_string" : "Contributions",
        "m_string" : "This page is on vacation",
        "m_code" : 404,
        "known" : ["john", "peter"],
        "cat" : "social"
       },
       {
        "name" : "Truth Social",
        "uri_check" : "https://truthsocial.com/api/v1/accounts/lookup?acct={account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_string" : "Record not found",
        "m_code" : 404,
        "known" : ["realdonaldtrump", "ScottAdamsTruth"],
        "cat" : "social"
       },
       {
        "name" : "TryHackMe",
        "uri_check" : "https://tryhackme.com/api/user/exist/{account}",
        "uri_pretty" : "https://tryhackme.com/r/p/{account}",
        "e_code" : 200,
        "e_string" : "\"success\":true",
        "m_string" : "\"success\":false",
        "m_code" : 200,
        "known" : ["user", "goyalyuval15"],
        "cat" : "tech"
       },
       {
        "name" : "Tryst",
        "uri_check" : "https://tryst.link/escort/{account}",
        "e_code" : 200,
        "e_string" : "Caters to</div>",
        "m_string" : "<title>Page not found",
        "m_code" : 404,
        "known" : ["lpatterson32", "kansasgirl69"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "tumblr",
        "uri_check" : "https://{account}.tumblr.com",
        "strip_bad_char" : ".",
        "e_code" : 200,
        "e_string" : "avatar",
        "m_string" : "There's nothing here",
        "m_code" : 404,
        "known" : ["test", "test1"],
        "cat" : "images"
       },
       {
        "name" : "Tunefind",
        "uri_check" : "https://www.tunefind.com/user/profile/{account}",
        "e_code" : 200,
        "e_string" : "Achievements",
        "m_string" : "Page not found",
        "m_code" : 404,
        "known" : ["baywolfmusic", "mrcerny18"],
        "cat" : "music"
       },
       {
        "name" : "Twitcasting",
        "uri_check" : "https://twitcasting.tv/{account}",
        "e_code" : 200,
        "e_string" : "Live History",
        "m_string" : "Not Found",
        "m_code" : 302,
        "known" : ["yuno___nico", "2_t0_"],
        "cat" : "social"
       },
       {
        "name" : "Twitch",
        "uri_check" : "https://twitchtracker.com/{account}",
        "uri_pretty" : "https://twitch.tv/{account}/",
        "e_code" : 200,
        "e_string" : "Overview</a>",
        "m_string" : "<title>404 Page Not Found",
        "m_code" : 404,
        "known" : ["summit1g", "cohhcarnage"],
        "cat" : "gaming"
       },
       {
        "name" : "Twitter",
        "uri_check" : "https://nitter.privacydev.net/{account}",
        "uri_pretty" : "https://twitter.com/{account}",
        "e_code" : 200,
        "e_string" : "| nitter</title>",
        "m_string" : "<title>Error |",
        "m_code" : 404,
        "known" : ["WebBreacher", "OSINT_Tactical"],
        "cat" : "social"
       },
       {
        "name" : "Twitter archived profile",
        "uri_check" : "http://archive.org/wayback/available?url=https://twitter.com/{account}",
        "uri_pretty" : "https://web.archive.org/web/2/https://twitter.com/{account}",
        "e_code" : 200,
        "e_string" : "\"archived_snapshots\": {\"closest\"",
        "m_string" : "\"archived_snapshots\": {}",
        "m_code" : 200,
        "known" : ["jack", "dineshdsouza"],
        "cat" : "archived"
       },
       {
        "name" : "Twitter archived tweets",
        "uri_check" : "http://archive.org/wayback/available?url=https://twitter.com/{account}/status/*",
        "uri_pretty" : "https://web.archive.org/web/*/https://twitter.com/{account}/status/*",
        "e_code" : 200,
        "e_string" : "\"archived_snapshots\": {\"closest\"",
        "m_string" : "\"archived_snapshots\": {}",
        "m_code" : 200,
        "known" : ["jack", "dineshdsouza"],
        "cat" : "archived"
       },
       {
        "name" : "twoplustwo",
        "uri_check" : "https://forumserver.twoplustwo.com/ajax.php?do=usersearch",
        "uri_pretty" : "https://forumserver.twoplustwo.com/search.php",
        "post_body" : "securitytoken=guest&do=usersearch&fragment={account}",
        "e_code" : 200,
        "e_string" : "userid=",
        "m_string" : "",
        "m_code" : 404,
        "known" : ["redsox", "adam"],
        "cat" : "hobby"
       },
       {
        "name" : "twpro",
        "uri_check" : "https://twpro.jp/{account}",
        "e_code" : 200,
        "e_string" : "おとなりさん",
        "m_code" : 404,
        "m_string" : "をご確認ください。",
        "known" : ["wsise47", "tsukiusa630"],
        "cat" : "social"
       },
       {
        "name" : "Ubisoft",
        "uri_check" : "https://discussions.ubisoft.com/user/{account}",
        "e_code" : 200,
        "e_string" : "| Ubisoft Discussion Forums",
        "m_string" : "You seem to have stumbled upon a page that does not exist.",
        "m_code" : 404,
        "known" : ["fizzle_fuze", "th05324"],
        "cat" : "gaming"
       },
       {
        "name" : "Udemy",
        "uri_check" : "https://www.udemy.com/user/{account}/",
        "e_code" : 200,
        "e_string" : "| Udemy</title>",
        "m_string" : "<title>Online Courses - Learn Anything, On Your Schedule | Udemy</title>",
        "m_code" : 301,
        "known" : ["stephane-maarek", "lizbrown3"],
        "cat" : "tech"
       },
       {
        "name" : "UEF CONNECT",
        "uri_check" : "https://uefconnect.uef.fi/en/{account}/",
        "e_code" : 200,
        "e_string" : "profile-page-header__info",
        "m_string" : "<title>Page not found - UEFConnect</title>",
        "m_code" : 404,
        "known" : ["heli.mutanen", "mette.heiskanen"],
        "cat" : "business"
       },
       {
        "name" : "uid",
        "uri_check" : "http://uid.me/{account}",
        "e_code" : 200,
        "e_string" : "- uID.me",
        "m_string" : "Page not found",
        "m_code" : 404,
        "known" : ["john", "peter"],
        "cat" : "social"
       },
       {
        "name" : "Ultimate Guitar",
        "uri_check" : "https://www.ultimate-guitar.com/u/{account}",
        "e_code" : 200,
        "e_string" : " | Ultimate-Guitar.Com</title>",
        "m_string" : "Oops! We couldn't find that page.",
        "m_code" : 410,
        "known" : ["LYNX-Music", "Mikhailo","MeGaDeth2314"],
        "cat" : "hobby"
       },
       {
        "name" : "Ultras Diary",
        "uri_check" : "http://ultrasdiary.pl/u/{account}/",
        "e_code" : 200,
        "e_string" : "Mecze wyjazdowe:",
        "m_string" : "Ile masz wyjazdów?",
        "m_code" : 404,
        "known" : ["janek", "kowal"],
        "cat" : "hobby"
       },
       {
        "name" : "Unlisted Videos",
        "uri_check" : "https://unlistedvideos.com/search.php?user={account}",
        "e_code" : 200,
        "e_string" : "Date submitted",
        "m_string" : "content=\"\"/>",
        "m_code" : 200,
        "known" : ["emudshit", "hirumaredx"],
        "cat" : "archived"
       },
       {
        "name" : "unsplash",
        "uri_check" : "https://unsplash.com/@{account}",
        "e_code" : 200,
        "e_string" : "| Unsplash Photo Community",
        "m_string" : "Hm, the page you were looking for doesn't seem to exist anymore.",
        "m_code" : 404,
        "known" : ["john", "alex"],
        "cat" : "images"
       },
       {
        "name" : "untappd",
        "uri_check" : "https://untappd.com/user/{account}/",
        "e_code" : 200,
        "e_string" : "on Untappd</title>",
        "m_string" : "Untappd | 404",
        "m_code" : 404,
        "known" : ["test", "phil"],
        "cat" : "social"
       },
       {
        "name" : "USA Life",
        "uri_check" : "https://usa.life/{account}",
        "e_code" : 200,
        "e_string" : "Please log in to like, share and comment",
        "m_string" : "Sorry, page not found",
        "m_code" : 302,
        "known" : ["abaynes79", "not1face"],
        "cat" : "social"
       },
       {
        "name" : "utip.io",
        "uri_check" : "https://utip.io/creator/profile/{account}",
        "uri_pretty" : "https://utip.io/{account}",
        "e_code" : 200,
        "e_string" : "\"userName\"",
        "m_code" : 404,
        "m_string" : "Not a valid web service key",
        "known" : ["honey", "chloe"],
        "cat" : "finance"
       },
       {
        "name" : "Uwumarket",
        "uri_check" : "https://uwumarket.us/collections/{account}",
        "e_code" : 200,
        "e_string" : "collection-hero__text-wrapper",
        "m_code" : 404,
        "m_string" : "Page not found",
        "known" : ["saki", "aicandii"],
        "cat" : "business"
       },
       {
        "name" : "uwu.ai",
        "uri_check" : "https://{account}.uwu.ai/",
        "strip_bad_char" : ".",
        "e_code" : 200,
        "e_string" : "property=\"twitter:card\"",
        "m_code" : 404,
        "m_string" : "Sorry, the requested page could not be found.",
        "known" : ["elite", "citruciel"],
        "cat" : "social"
       },
       {
        "name" : "vapenews",
        "uri_check" : "https://vapenews.ru/profile/{account}",
        "e_code" : 200,
        "e_string" : "<title inertia>Профиль</title></head>",
        "m_string" : "<title>404</title>",
        "m_code" : 404,
        "known" : ["igor", "vladimir"],
        "cat" : "hobby"
       },
       {
        "name" : "vsco",
        "uri_check" : "https://vsco.co/{account}/gallery",
        "e_code" : 200,
        "e_string" : "permaSubdomain",
        "m_string" : "\"error\":\"site_not_found\"}",
        "m_code" : 404,
        "known" : ["sam", "becca"],
        "cat" : "social",
        "headers" : {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0"}
       },
       {
        "name" : "Venmo",
        "uri_check" : "https://account.venmo.com/u/{account}",
        "e_code" : 200,
        "e_string" : "profileInfo_username__",
        "m_string" : "Sorry, the page you requested does not exist!",
        "m_code" : 404,
        "known" : ["John-Goolsby-8", "kate-mura"],
        "cat" : "finance"
       },
       {
        "name" : "Vero",
        "uri_check" : "https://vero.co/{account}",
        "e_code" : 200,
        "e_string" : "on VERO™</title>",
        "m_string" : "The page you are looking for doesn't exist.",
        "m_code" : 404,
        "known" : ["alex", "johnny"],
        "cat" : "art"
       },
       {
        "name" : "vibilagare",
        "uri_check" : "https://www.vibilagare.se/users/{account}",
        "e_code" : 200,
        "e_string" : "Profil på vibilagare.se",
        "m_string" : "Sidan hittades inte |",
        "m_code" : 404,
        "known" : ["lars01", "sven"],
        "cat" : "misc"
       },
       {
        "name" : "viddler",
        "uri_check" : "https://www.viddler.com/channel/{account}/",
        "e_code" : 200,
        "e_string" : "profile-details",
        "m_string" : "User not found",
        "m_code" : 404,
        "known" : ["GamingParodies", "planphilly"],
        "cat" : "video"
       },
       {
        "name" : "Viewbug",
        "uri_check" : "https://www.viewbug.com/member/{account}",
        "e_code" : 200,
        "e_string" : "s Photos - VIEWBUG.com </title>",
        "m_string" : "<title>Missing Page - VIEWBUG.com",
        "m_code" : 404,
        "known" : ["joe", "evgeniyflor"],
        "cat" : "hobby"
       },
       {
        "name" : "Vimeo",
        "uri_check" : "https://vimeo.com/{account}",
        "e_code" : 200,
        "e_string" : "og:type",
        "m_string" : "VimeUhOh",
        "m_code" : 404,
        "known" : ["john", "alice"],
        "cat" : "video"
       },
       {
        "name" : "Vine",
        "uri_check" : "https://vine.co/api/users/profiles/vanity/{account}",
        "uri_pretty" : "https://vine.co/{account}",
        "e_code" : 200,
        "e_string" : "userId",
        "m_string" : "That record does not exist",
        "m_code" : 404,
        "known" : ["TomHarlock", "Seks"],
        "cat" : "video"
       },
       {
        "name" : "visnesscard",
        "uri_check" : "https://my.visnesscard.com/Home/GetCard/{account}",
        "uri_pretty" : "https://my.visnesscard.com/{account}",
        "e_code" : 200,
        "e_string" : "end_point",
        "m_string" : "card_id\": 0",
        "m_code" : 200,
        "known" : ["Lisa-Gordon", "Bill-Schaeffer"],
        "cat" : "business"
       },
       {
        "name" : "Vivino",
        "uri_check" : "https://www.vivino.com/users/{account}",
        "e_code" : 200,
        "e_string" : "<!-- User details -->",
        "m_string" : "Page not found",
        "m_code" : 404,
        "known" : ["test", "admin"],
        "cat" : "video"
      },
      {
        "name" : "VIP-blog",
        "uri_check" : "http://{account}.vip-blog.com",
        "strip_bad_char" : ".",
        "e_code" : 200,
        "e_string" : "blog : ",
        "m_string" : "Blog inexistant",
        "m_code" : 200,
        "known" : ["sarah", "brahim01"],
        "cat" : "blog"
      },
      {
        "name" : "VirusTotal",
        "uri_check" : "https://www.virustotal.com/ui/users/{account}",
        "uri_pretty" : "https://www.virustotal.com/gui/user/{account}",
        "headers" : {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
                "X-Tool": "vt-ui-main",
                "Accept-Ianguage": "en-US",
                "X-VT-Anti-Abuse-Header": "MTAxOTFwMDcxOTEtWkc5dWRDQmlaU0JsZG2scy5xNzE4Mjc1NDI0LjUzMw=="
        },
        "e_code" : 200,
        "e_string" :"\"data\"",
        "m_string" : "\"code\": \"NotFoundError\"",
        "m_code" : 404,
        "known" : ["cyber", "cybersecstu"],
        "cat" : "misc"
       },
       {
        "name" : "VK",
        "uri_check" : "https://vk.com/{account}",
        "e_code" : 200,
        "e_string" : "content=\"profile\"",
        "m_string" : "404 Not Found",
        "m_code" : 404,
        "known" : ["ches_ches", "mike.kidlazy"],
        "cat" : "social",
        "headers" : {
          "User-Agent" : "Mozilla/5.0 (X11; Linux i686; rv:125.0) Gecko/20100101 Firefox/125.0"
        }
       },
       {
        "name" : "Vkl.world (Mastodon Instance)",
        "uri_check" : "https://vkl.world/api/v1/accounts/lookup?acct={account}",
        "uri_pretty" : "https://vkl.world/@{account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_code" : 404,
        "m_string" : "Record not found",
        "known" : ["king", "aniver"],
        "cat" : "social"
       },
       {
        "name" : "Vmst.io (Mastodon Instance)",
        "uri_check" : "https://vmst.io/api/v1/accounts/lookup?acct={account}",
        "uri_pretty" : "https://vmst.io/@{account}",
        "e_code" : 200,
        "e_string" : "display_name",
        "m_code" : 404,
        "m_string" : "Record not found",
        "known" : ["vmstan", "honestdave"],
        "cat" : "social"
       },
       {
        "name" : "Voice123",
        "uri_check" : "https://voice123.com/api/providers/search/{account}",
        "uri_pretty" : "https://voice123.com/{account}",
        "e_code" : 200,
        "e_string" : "user_id",
        "m_code" : 200,
        "m_string" : "[]",
        "known" : ["dottovuu", "maheshsaha1992"],
        "cat" : "hobby"
       },
       {
        "name" : "Voices.com",
        "uri_check" : "https://www.voices.com/profile/{account}/",
        "e_code" : 200,
        "e_string" : "Last Online</h3>",
        "m_string" : "Try going back to the previous page or see below for more options",
        "m_code" : 301,
        "known" : ["briankirchoff", "bryankopta"],
        "cat" : "business"
       },
       {
        "name" : "watchmemore.com",
        "uri_check" : "https://api.watchmemore.com/api4/profile/{account}/",
        "uri_pretty" : "https://watchmemore.com/{account}/",
        "e_code" : 200,
        "e_string" : "displayName",
        "m_string" : "notExists",
        "m_code" : 400,
        "known" : ["medroxy", "nodjev"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "Warmerise",
        "uri_check" : "https://warmerise.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "<div id='profile_photo",
        "m_string" : "<h2>Page Not Found",
        "m_code" : 404,
        "known" : ["alfrevid", "thepro"],
        "cat" : "gaming"
       },
       {
        "name" : "warriorforum",
        "uri_check" : "https://www.warriorforum.com/members/{account}.html",
        "e_code" : 200,
        "e_string" : "Last Activity:",
        "m_string" : "Oops | Warrior Forum -",
        "m_code" : 400,
        "known" : ["alex", "discrat"],
        "cat" : "hobby"
       },
       {
        "name" : "Watchmyfeed",
        "uri_check" : "https://watchmyfeed.com/{account}",
        "e_code" : 200,
        "e_string" : "SEND ME A TIP",
        "m_string" : "",
        "m_code" : 302,
        "known" : ["jennifer-ann", "shay-loveless"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "Wattpad",
        "uri_check" : "https://www.wattpad.com/api/v3/users/{account}",
        "uri_pretty" : "https://www.wattpad.com/user/{account}",
        "e_code" : 200,
        "e_string" : "\"username\":",
        "m_string" : "\"error_code\":",
        "m_code" : 400,
        "known" : ["newadult", "Test123"],
        "cat" : "social",
        "protection" : ["other"]
       },
       {
        "name" : "Weasyl",
        "uri_check" : "https://www.weasyl.com/~{account}",
        "e_code" : 200,
        "e_string" : "profile — Weasyl</title>",
        "m_string" : "This user doesn't seem to be in our database.",
        "m_code" : 404,
        "known" : ["weasyl", "test"],
        "cat" : "images"
       },
       {
        "name" : "weebly",
        "uri_check" : "https://{account}.weebly.com/",
        "strip_bad_char" : ".",
        "e_code" : 200,
        "e_string" : "<div id=\"navigation\">",
        "m_string" : "<title>404 - Page Not Found",
        "m_code" : 404,
        "known" : ["dave", "john"],
        "cat" : "misc"
       },
       {
        "name" : "Weblancer",
        "uri_check" : "https://www.weblancer.net/users/{account}/",
        "e_code" : 200,
        "e_string" : "\"user\":",
        "m_string" : "\"page\":\"/404\"",
        "m_code" : 404,
        "known" : ["kevin", "WebArtyom"],
        "cat" : "social",
        "headers" : {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0"}
       },
       {
        "name" : "weheartit",
        "uri_check" : "https://weheartit.com/{account}",
        "e_code" : 200,
        "e_string" : " on We Heart It</title>",
        "m_string" : " (404)</title>",
        "m_code" : 404,
        "known" : ["alice", "bob"],
        "cat" : "social"
       },
       {
        "name" : "wego",
        "uri_check" : "https://wego.social/{account}",
        "e_code" : 200,
        "e_string" : "Following</span>",
        "m_string" : "Sorry, page not found!",
        "m_code" : 302,
        "known" : ["mmish2", "Lisa_M_S"],
        "cat" : "political"
       },
       {
        "name" : "weibo",
        "uri_check" : "https://tw.weibo.com/{account}",
        "e_code" : 200,
        "e_string" : "粉絲",
        "m_string" : "Oops!",
        "m_code" : 404,
        "known" : ["chentingni", "fbb0916"],
        "cat" : "social"
       },
       {
        "name" : "WeTransfer",
        "uri_check" : "https://{account}.wetransfer.com",
        "strip_bad_char" : ".",
        "e_code" : 200,
        "e_string" : "workspaceName",
        "m_string" : "",
        "m_code" : 307,
        "known" : ["mark", "joe"],
        "cat" : "misc"
       },
       {
        "name" : "Wikidot",
        "uri_check" : "http://www.wikidot.com/user:info/{account}",
        "e_code" : 200,
        "e_string" : "Wikidot.com:",
        "m_string" : "Free and Pro Wiki Hosting",
        "m_code" : 404,
        "known" : ["jack", "allen"],
        "cat" : "social"
       },
       {
        "name" : "Wikimapia",
        "uri_check" : "https://wikimapia.org/user/register/?check=username&value={account}",
        "uri_pretty" : "https://wikimapia.org/user/tools/users_rating/?username={account}",
        "e_code" : 200,
        "e_string" : "\"ok\":false",
        "m_string" : "\"ok\":true",
        "m_code" : 200,
        "known" : ["bubnilka", "Teresa"],
        "cat" : "social"
       },
       {
        "name" : "Wikipedia",
        "uri_check" : "https://meta.wikimedia.org/w/api.php?action=query&format=json&list=globalallusers&aguprefix={account}&agulimit=100",
        "uri_pretty" : "https://en.wikipedia.org/wiki/User:{account}",
        "e_code" : 200,
        "e_string" : "{\"id\":",
        "m_string" : ":[]}}",
        "m_code" : 200,
        "known" : ["sector051", "webbreacher"],
        "cat" : "news"
       },
       {
        "name" : "Wimkin-PublicProfile",
        "uri_check" : "https://wimkin.com/{account}",
        "e_code" : 200,
        "e_string" : "is on WIMKIN",
        "m_string" : " The page you are looking for cannot be found.",
        "m_code" : 404,
        "known" : ["alex", "smith", "boomer"],
        "cat" : "political"
       },
       {
        "name" : "Wireclub",
        "uri_check" : "https://www.wireclub.com/users/{account}",
        "e_code" : 200,
        "e_string" : "Chat With",
        "m_string" : "People - Wireclub",
        "m_code" : 301,
        "known" : ["deae", "cheerfulsarcasm", "braydenskiresort"],
        "cat" : "social",
        "protection" : ["other"]
       },
       {
        "name" : "Wakatime",
        "uri_check" : "https://wakatime.com/@{account}",
        "e_code" : 200,
        "e_string" : ") - WakaTime</title>",
        "m_string" : "<title>404: Not Found",
        "m_code" : 404,
        "known" : ["jake", "alimirzayev"],
        "cat" : "coding"
       },
       {
        "name" : "wishlistr",
        "uri_check" : "https://www.wishlistr.com/profile/{account}/",
        "e_code" : 200,
        "e_string" : "s profile</title>",
        "m_string" : "",
        "m_code" : 302,
        "known" : ["test"],
        "cat" : "shopping"
       },
       {
        "name" : "wordnik",
        "uri_check" : "https://www.wordnik.com/users/{account}",
        "e_code" : 200,
        "e_string" : "Welcome,",
        "m_string" : "Wordnik: Page Not Found",
        "m_code" : 404,
        "known" : ["elle", "john"],
        "cat" : "gaming"
       },
       {
        "name" : "WordPress",
        "uri_check" : "https://profiles.wordpress.org/{account}/",
        "e_code" : 200,
        "e_string" : "user-member-since",
        "m_string" : "",
        "m_code" : 404,
        "known" : ["test"],
        "cat" : "blog"
       },
       {
        "name" : "WordPress Support",
        "uri_check" : "https://wordpress.org/support/users/{account}/",
        "e_code" : 200,
        "e_string" : "s Profile &#124; WordPress.org",
        "m_string" : "User not found",
        "m_code" : 404,
        "known" : ["test"],
        "cat" : "blog"
       },
       {
        "name" : "Wowhead",
        "uri_check" : "https://www.wowhead.com/user={account}",
        "e_code" : 200,
        "e_string" : " Profile - Wowhead",
        "m_string" : "Error - Wowhead",
        "m_code" : 404,
        "known" : ["Ashelia", "Zizarz"],
        "cat" : "gaming"
       },
       {
        "name" : "Wykop",
        "uri_check" : "https://wykop.pl/ludzie/{account}",
        "e_code" : 200,
        "e_string" : "<title>Profil:",
        "m_string" : "Wystąpił błąd 404.",
        "m_code" : 404,
        "known" : ["test", "test2"],
        "cat" : "social"
       },
       {
        "name" : "Xakep.ru",
        "uri_check" : "https://xakep.ru/author/{account}/",
        "e_code" : 200,
        "e_string" : "authorBlock-avatar",
        "m_string" : "Страница не найдена",
        "m_code" : 404,
        "known" : ["tr3harder", "stariy"],
        "cat" : "tech"
       },
       {
        "name" : "Xanga",
        "uri_check" : "http://{account}.xanga.com/",
        "strip_bad_char" : ".",
        "e_code" : 200,
        "e_string" : "s Xanga Site | Just",
        "m_string" : "",
        "m_code" : 302,
        "known" : ["john"],
        "cat" : "blog"
       },
       {
        "name" : "Xbox Gamertag",
        "uri_check" : "https://www.xboxgamertag.com/search/{account}",
        "e_code" : 200,
        "e_string" : "Games Played",
        "m_string" : "Gamertag doesn't exist",
        "m_code" : 404,
        "known" : ["Spiken8", "john"],
        "cat" : "gaming"
       },
       {
        "name" : "xHamster",
        "uri_check" : "https://xhamster.com/users/{account}",
        "e_code" : 200,
        "e_string" : "s profile | xHamster</title>",
        "m_string" : "User not found</title>",
        "m_code" : 404,
        "known" : ["john", "tonystark85"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "Xing",
        "uri_check" : "https://www.xing.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "<meta data-rh=",
        "m_string" : "404 Not Found | XING",
        "m_code" : 404,
        "known" : ["Andy_Hausmann", "Stephan_Abele2"],
        "cat" : "social"
       },
       {
         "name" : "XNXX",
         "uri_check" : "https://www.xnxx.com/mobile/profile/{account}",
         "e_code" : 200,
         "e_string" : "<table id=\"profile\">",
         "m_string" : "<title>Bad request",
         "m_code" : 400,
         "known" : ["john", "mumrra"],
         "cat" : "xx NSFW xx"
       },
       {
        "name" : "XVIDEOS-models",
        "uri_check" : "https://www.xvideos.com/models/{account}",
        "e_code" : 200,
        "e_string" : "Total video views",
        "m_string" : "THIS PROFILE DOESN'T EXIST",
        "m_code" : 404,
        "known" : ["vvalencourt3", "tiffany-tyler"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "XVIDEOS-profiles",
        "uri_check" : "https://www.xvideos.com/profiles/{account}",
        "e_code" : 200,
        "e_string" : "page - XVIDEOS.COM",
        "m_string" : "THIS PROFILE DOESN'T EXIST",
        "m_code" : 404,
        "known" : ["nympho-nailer", "dpadicto", "bkg"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "Yahoo! JAPAN Auction",
        "uri_check" : "https://auctions.yahoo.co.jp/follow/list/{account}",
        "e_code" : 200,
        "e_string" : "出品者",
        "m_code" : 500,
        "m_string" : "Yahoo! JAPAN IDが無効です。",
        "known" : ["fltr14502003"],
        "cat" : "shopping"
       },
       {
       "name" : "yapishu",
       "uri_check" : "https://yapishu.net/user/{account}",
       "e_code" : 200,
       "e_string" : "for_profile",
       "m_string" : "Not Found (#404)",
       "m_code" : 404,
       "known" : ["roman", "semion"],
       "cat" : "hobby"
       },
       {
        "name" : "Yazawaj",
        "uri_check" : "https://www.yazawaj.com/profile/{account}",
        "e_code" : 200,
        "e_string" : "profile-description",
        "m_string" : "<title>nodata",
        "m_code" : 302,
        "known" : ["monya14555d", "LordMohy"],
        "cat" : "dating"
       },
       {
        "name" : "Yelp",
        "uri_check" : "https://www.yelp.com/user_details?userid={account}",
        "e_code" : 200,
        "e_string" : "'s Reviews |",
        "m_string" : "Doggone it! The page you’re looking for cannot be found.",
        "m_code" : 404,
        "known" : ["j5CYhsvD2yrunyyoZvSvKA", "GHoG4X4FY8D8L563zzPX5w"],
        "cat" : "shopping"
       },
       {
        "name" : "YesWeHack",
        "uri_check" : "https://api.yeswehack.com/hunters/{account}",
        "uri_pretty" : "https://yeswehack.com/hunters/{account}",
        "e_code" : 200,
        "e_string" : "\"username\":",
        "m_string" : "\"code\":404",
        "m_code" : 404,
        "known" : ["xel", "rabhi"],
        "cat" : "tech"
       },
       {
        "name" : "youpic",
        "uri_check" : "https://youpic.com/photographer/{account}",
        "e_code" : 200,
        "e_string" : "<meta name=\"og:title\"",
        "m_string" : "<title>YouPic — Not Found</title>",
        "m_code" : 404,
        "known" : ["photodude", "mike"],
        "cat" : "hobby"
       },
       {
        "name" : "YouNow",
        "uri_check" : "https://api.younow.com/php/api/broadcast/info/user={account}",
        "uri_pretty" : "https://www.younow.com/{account}",
        "e_code" : 200,
        "e_string" : "\"userId\":",
        "m_string" : "\"errorMsg\":\"No users found\"",
        "m_code" : 200,
        "known" : ["lydia_tan33", "RavJagz"],
        "cat" : "social",
        "protection" : ["other"]
       },
       {
        "name" : "YouTube Channel",
        "uri_check" : "https://www.youtube.com/c/{account}/about",
        "e_code" : 200,
        "e_string" : "joinedDateText",
        "m_string" : "<title>404 Not Found",
        "m_code" : 404,
        "known" : ["OvylarockTHR","OSINTDojo"],
        "cat" : "video"
       },
       {
        "name" : "YouTube User",
        "uri_check" : "https://www.youtube.com/user/{account}/about",
        "e_code" : 200,
        "e_string" : "joinedDateText",
        "m_string" : "<title>404 Not Found",
        "m_code" : 404,
        "known" : ["MicahHoffman","theosintcuriousproject"],
        "cat" : "video"
       },
       {
        "name" : "YouTube User2",
        "uri_check" : "https://www.youtube.com/@{account}",
        "e_code" : 200,
        "e_string" : "canonicalBaseUrl",
        "m_string" : "<title>404 Not Found</title>",
        "m_code" : 404,
        "known" : ["tactical-systems","CybersecurityMeg"],
        "cat" : "video"
       },
       {
        "name" : "Zbiornik",
        "uri_check" : "https://mini.zbiornik.com/{account}",
        "e_code" : 200,
        "e_string" : "INFO",
        "m_string" : "",
        "m_code" : 301,
        "known" : ["69uzytkownik69", "Soif"],
        "cat" : "xx NSFW xx",
        "headers" : {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0"}
       },
       {
        "name" : "Zenn",
        "uri_check" : "https://zenn.dev/{account}",
        "e_code" : 200,
        "e_string" : "<div class=\"UserHeader_profileMain__6Itxi\">",
        "m_string" : "<div class=\"ErrorContent_status__2Ykoq\">404</div>",
        "m_code" : 404,
        "known" : ["john", "blue"],
        "cat" : "coding"
      },
       {
        "name" : "Zepeto",
        "uri_pretty" : "https://web.zepeto.me/share/user/profile/{account}?language=en",
        "uri_check" : "https://gw-napi.zepeto.io/profiles/{account}",
        "e_code" : 200,
        "e_string" : "zepetoId\":",
        "m_string" : "errorCode\":",
        "m_code" : 200,
        "known" : ["joe", "james"],
        "cat" : "social"
       },
       {
        "name" : "zhihu",
        "uri_check" : "https://api.zhihu.com/books/people/{account}/publications?offset=0&limit=5",
        "uri_pretty" : "https://www.zhihu.com/people/{account}",
        "e_code" : 200,
        "e_string" : "\"is_start\": true",
        "m_string" : "\"name\": \"NotFoundException\"",
        "m_code" : 404,
        "known" : ["lushnis", "kan-shu-jiao-hua-shai-tai-yang"],
        "cat" : "social"
       },
       {
        "name" : "Zillow",
        "uri_check" : "https://www.zillow.com/profile/{account}/",
        "e_code" : 200,
        "e_string" : "- Real Estate Agent",
        "m_string" : "",
        "m_code" : 302,
        "known" : ["JOHN-L-SULLIVAN", "Maggie-Alegria"],
        "cat" : "shopping"
       },
       {
        "name" : "zmarsa.com",
        "uri_check" : "https://zmarsa.com/uzytkownik/{account}",
        "e_code" : 200,
        "e_string" : "Statystyki",
        "m_string" : "<title>Error 404 - zMarsa.com<",
        "m_code" : 404,
        "known" : ["janek", "test"],
        "cat" : "xx NSFW xx"
       },
       {
        "name" : "Zomato",
        "uri_check" : "https://www.zomato.com/{account}/reviews",
        "e_code" : 200,
        "e_string" : "Activity</h4>",
        "m_string" : "This is a 404 page and we think it's fairly clear",
        "m_code" : 404,
        "known" : ["john", "jess"],
        "cat" : "social",
        "headers" : {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0"}
       },
       {
        "name" : "zoomitir",
        "uri_check" : "https://www.zoomit.ir/user/{account}/",
        "e_code" : 301,
        "e_string" : "",
        "m_string" : "<title>خطای ۴۰۴ - صفحه یافت نشد</title>",
        "m_code" : 404,
        "known" : ["rezaghezi", "hosssssein"],
        "cat" : "tech"
       }
  ]
}

user_agents = working_user_agents = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9",
    "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/7.1.8 Safari/537.85.17",
    "Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4",
    "Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F69 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS x86_64 7077.134.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.156 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/7.1.7 Safari/537.85.16",
    "Mozilla/5.0 (Windows NT 6.0; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.18",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B440 Safari/600.1.4",
    "Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; KFTT Build/IML74K) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12D508 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0",
    "Mozilla/5.0 (iPad; CPU OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53",
    "Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/7.1.6 Safari/537.85.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.4.10 (KHTML, like Gecko) Version/8.0.4 Safari/600.4.10",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2",
    "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12H321 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4",
    "Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53",
    "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; TNJB; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; ARM; Trident/7.0; Touch; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MDDCJS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4",
    "Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFASWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12H321 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MATBJS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; KFJWI Build/IMM76D) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D167 Safari/9537.53",
    "Mozilla/5.0 (X11; CrOS armv7l 7077.134.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.156 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.2.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56",
    "Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFSOWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko)"
]

def get_random_user_agent():
    return random.choice(user_agents)

def check_username_on_website(site, username):
    try:
        url = site["uri_check"].replace("{account}", username)
        headers = {"User-Agent": get_random_user_agent()}
        response = requests.get(url, headers=headers, timeout=10)
	    
        if (response.status_code == site["e_code"] and 
            site["e_string"] in response.text):
            return (site["name"], url)
        elif (response.status_code == site["m_code"] and 
              site["m_string"] in response.text):
            return None
        return None

    except Exception as e:
        return None

def scrape_duckduckgo_links(query):
    url = f"https://duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": get_random_user_agent()}

    try:
        response = requests.get(url, headers=headers, timeout=6)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        links = set()  

        for a_tag in soup.find_all("a", class_="result__a", href=True):
            href = a_tag.get("href")

            if "duckduckgo.com/l/?" in href:
                parsed_url = urlparse(href)
                real_url = parse_qs(parsed_url.query).get("uddg", [None])[0]
                if real_url:
                    links.add(real_url)  
            elif "duckduckgo.com" not in href:  
                links.add(href)  

        return list(links)[:12]  # limit links to scan

    except requests.exceptions.RequestException as e:
        print(f"\033[91mError with DuckDuckGo request: {e}\033[0m")
        return []

def search_username(username, threads=500):  
    start_time = time.time()  
    print(f"\n\033[38;2;255;255;255mChecking username {username} \033[38;2;57;255;20mon:\n")
    
    found = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(check_username_on_website, site, username): site 
                   for site in metadata["sites"]}
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                found.append(result)

    duckduckgo_results = scrape_duckduckgo_links(username)
    elapsed_time = time.time() - start_time

    if found or duckduckgo_results:
        if found:
            print(f"\033[38;2;255;255;0mFound Matches:")
            unique_sites = set()
            for site_name, url in found:
                if site_name not in unique_sites:
                    unique_sites.add(site_name)
                    site_metadata = next((site for site in metadata["sites"] if site["name"] == site_name), None)
                    category = site_metadata["cat"] if site_metadata else "Unknown"
                    print(f"\033[38;5;81m{site_name:<20} \033[38;2;213;166;209m[{category}] \033[38;2;255;255;255m {url}")

        if duckduckgo_results:
            print(f"\n\033[38;2;255;255;0m🦆 DuckDuckGo {len(duckduckgo_results)} results):")
            for i, link in enumerate(duckduckgo_results, 1):
                print(f"\033[38;2;57;255;20m[\033[38;5;81m{i}\033[38;2;57;255;20m]\033[38;2;255;255;255m {link}")  

        print(f"\n\033[38;2;255;255;255mSummary:")
        print(f"\033[38;2;255;255;0m🔎 Websites found: {len(found)}")
        print(f"\033[38;2;255;255;0m🏁 Total time: {elapsed_time:.2f} seconds")
    else:
        print(f"\n\033[91mNo matches found\033[0m")
        print(f"\033[38;2;255;255;0m🏁 Total time: {elapsed_time:.2f} seconds")



if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    
    print("""\033[38;2;255;255;0m
   _____   ______________  ______  _________
   ___  | / /__  ____/_  |/ /_  / / /_  ___/
   __   |/ /__  __/  __    /_  / / /_____ \ 
   _  /|  / _  /___  _    | / /_/ / ____/ / 
   /_/ |_/  /_____/  /_/|_| \____/  /____/                                                                     
    """)
    print(Fore.WHITE+"> Created By biskit")

    username = input(f"""
\033[38;2;255;255;0mUsername~$\033[38;2;255;255;255m """)
    
    search_username(username)
