{-# LANGUAGE OverloadedStrings #-}

module Main (main) where

import Data.Monoid (mappend, (<>))
import Hakyll

main :: IO ()
main =
  hakyll $ do
    tags <- buildTags "posts/*" (fromCapture "tags/*.html")

    match "templates/*" (compile templateCompiler)

    match "images/*" $ do
      route idRoute
      compile copyFileCompiler

    match "css/*" $ do
      route idRoute
      compile compressCssCompiler

    match (fromList ["about.md", "contact.md"]) $ do
      route (setExtension "html")
      compile $ pandocCompiler
        >>= loadAndApplyTemplate "templates/default.html" defaultContext
        >>= relativizeUrls

    -- tags
    tagsRules tags $ \tag pattern -> do
        let title = "Posts tagged \"" ++ tag ++ "\""
        route idRoute
        compile $ do
          posts <- recentFirst =<< loadAll pattern
          let ctx = constField "title" title <>
                    listField "posts" postContext (return posts) <>
                    defaultContext
          makeItem ""
                    >>= loadAndApplyTemplate "templates/tag.html" ctx
                    >>= loadAndApplyTemplate "templates/default.html" ctx
                    >>= relativizeUrls
    -- posts
    match "posts/*" $ do
      route (setExtension "html")
      compile $ pandocCompiler
        >>= saveSnapshot "content-for-teaser"
        >>= loadAndApplyTemplate "templates/post.html" (postContextWithTags tags)
        >>= saveSnapshot "feed-post-content"
        >>= loadAndApplyTemplate "templates/default.html" (postContextWithTags tags)
        >>= relativizeUrls

    -- index
    match "index.html" $ do
      route idRoute
      compile $ do
        posts <- recentFirst =<< loadAllSnapshots  "posts/*" "content-for-teaser"
        let indexContext =
              listField "posts" (postContextWithTeaser tags) (return posts) <>
              constField "title" "Home" <>
              defaultContext

        getResourceBody
          >>= applyAsTemplate indexContext
          >>= loadAndApplyTemplate "templates/default.html" indexContext
          >>= relativizeUrls

    -- feeds
    create ["feed.xml"] $ do
      route idRoute
      compile $ do
        posts <- fmap (take 10) . recentFirst
                   =<< loadAllSnapshots "posts/*" "feed-post-content"
        renderAtom feedConfiguration feedContext posts

    create ["rss.xml"] $ do
      route idRoute
      compile $ do
        posts <- fmap (take 10) . recentFirst
                   =<< loadAllSnapshots "posts/*" "feed-post-content"
        renderRss feedConfiguration feedContext posts

feedContext :: Context String
feedContext =
  postContext <> bodyField "description"

postContext :: Context String
postContext =
  dateField "date" "%Y-%m-%d" <>
  defaultContext

postContextWithTags :: Tags -> Context String
postContextWithTags tags =
  tagsField "tags" tags <>
  postContext

postContextWithTeaser :: Tags -> Context String
postContextWithTeaser tags =
  teaserField "teaser" "content-for-teaser" <>
  (postContextWithTags tags)

feedConfiguration :: FeedConfiguration
feedConfiguration =
  FeedConfiguration
    { feedTitle = "Cascade Of Insights"
    , feedDescription = "Adam Bell's blog"
    , feedAuthorName = "Adam Bell"
    , feedAuthorEmail = "agbell at gmail.com"
    , feedRoot = ""
    }
