{-# LANGUAGE OverloadedStrings #-}

module Main (main) where

import Data.Monoid (mappend)
import Hakyll

main :: IO ()
main =
  hakyll $ do
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
    -- build up tags
    tags <- buildTags "posts/*" (fromCapture "tags/*.html")
    tagsRules tags $ \tag pattern -> do
        let title = "Posts tagged \"" ++ tag ++ "\""
        route idRoute
        compile $ do
          posts <- recentFirst =<< loadAll pattern
          let ctx = constField "title" title
                    `mappend` listField "posts" postContext (return posts)
                    `mappend` defaultContext
          makeItem ""
                    >>= loadAndApplyTemplate "templates/tag.html" ctx
                    >>= loadAndApplyTemplate "templates/default.html" ctx
                    >>= relativizeUrls
    match "posts/*" $ do
      route (setExtension "html")
      compile $ pandocCompiler
        >>= loadAndApplyTemplate "templates/post.html" (postContextWithTags tags)
        >>= saveSnapshot "content"
        >>= loadAndApplyTemplate "templates/default.html" (postContextWithTags tags)
        >>= relativizeUrls

    create ["archive.html"] $ do
      route idRoute
      compile $ do
        posts <- recentFirst =<< loadAll "posts/*"
        let archiveContext =
              listField "posts" postContext (return posts) `mappend`
              constField "title" "Archives" `mappend`
              defaultContext

        makeItem ""
          >>= loadAndApplyTemplate "templates/archive.html" archiveContext
          >>= loadAndApplyTemplate "templates/default.html" archiveContext
          >>= relativizeUrls

    match "index.html" $ do
      route idRoute
      compile $ do
        posts <- recentFirst =<< loadAll "posts/*"
        let indexContext =
              listField "posts" postContext (return posts) `mappend`
              constField "title" "Home" `mappend`
              defaultContext

        getResourceBody
          >>= applyAsTemplate indexContext
          >>= loadAndApplyTemplate "templates/default.html" indexContext
          >>= relativizeUrls

    match "templates/*" (compile templateCompiler)

    create ["atom.xml"] $ do
      route idRoute
      compile $ do
        posts <- fmap (take 10) . recentFirst
                   =<< loadAllSnapshots "posts/*" "content"
        renderAtom feedConfiguration feedContext posts

    create ["rss.xml"] $ do
      route idRoute
      compile $ do
        posts <- fmap (take 10) . recentFirst
                   =<< loadAllSnapshots "posts/*" "content"
        renderRss feedConfiguration feedContext posts

feedContext :: Context String
feedContext =
  postContext `mappend` bodyField "description"

postContext :: Context String
postContext =
  dateField "date" "%Y-%m-%d" `mappend` defaultContext

postContextWithTags :: Tags -> Context String
postContextWithTags tags = tagsField "tags" tags `mappend` postContext

feedConfiguration :: FeedConfiguration
feedConfiguration =
  FeedConfiguration
    { feedTitle = "Cascade Of Insights"
    , feedDescription = "Adam Bell's blog"
    , feedAuthorName = "Adam Bell"
    , feedAuthorEmail = "agbell at gmail.com"
    , feedRoot = ""
    }
