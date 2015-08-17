{-# LANGUAGE OverloadedStrings #-}

module Main (main) where

import Hakyll
import Hakyll.Web.Paginate
import Data.List
import Data.Monoid (mappend, (<>))
import Data.Functor ((<$>))

main :: IO ()
main =
  hakyll $ do
    tags <- buildTags "posts/**" (fromCapture "tags/*.html")
    pages <- buildPages "posts/**"
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

    -- posts
    match "posts/**" $ do
      route (setExtension "html")
      compile $ pandocCompiler
        >>= saveSnapshot "content-for-teaser"
        >>= loadAndApplyTemplate "templates/post.html" (postContextWithTags tags)
        >>= saveSnapshot "feed-post-content"
        >>= loadAndApplyTemplate "templates/default.html" (postContextWithTags tags)
        >>= relativizeUrls


    -- tags
    tagsRules tags $ \tag pattern -> do
        let title = "Posts tagged \"" ++ tag ++ "\""
        route idRoute
        compile $ do
          posts <- recentFirstNonDrafts =<< loadAll pattern
          let ctx = constField "title" title <>
                    listField "posts" postContext (return posts) <>
                    defaultContext
          makeItem ""
                    >>= loadAndApplyTemplate "templates/tag.html" ctx
                    >>= loadAndApplyTemplate "templates/default.html" ctx
                    >>= relativizeUrls

    -- index and paged listing
    paginateRules pages $ \index pattern -> do
        route $ setExtension "html"
        compile $ makeItem ""
            >>= loadAndApplyTemplate "templates/post-list.html" (indexContext index pages tags)
            >>= loadAndApplyTemplate "templates/default.html" (indexContext index pages tags)
            >>= relativizeUrls

    -- archive
    create ["archive.html"] $ do
      route idRoute
      compile $ do
        posts <- recentFirstNonDrafts =<< loadAll "posts/**"
        let archiveContext =
              listField "posts" postContext (return posts) `mappend`
              constField "title" "Archives" `mappend`
              defaultContext

        makeItem ""
          >>= loadAndApplyTemplate "templates/archive.html" archiveContext
          >>= loadAndApplyTemplate "templates/default.html" archiveContext
          >>= relativizeUrls

    -- feeds
    create ["feed.xml"] $ do
      route idRoute
      compile $ do
        posts <- fmap (take 10) . recentFirstNonDrafts
                   =<< loadAllSnapshots "posts/**" "feed-post-content"
        renderAtom feedConfiguration feedContext posts

    create ["rss.xml"] $ do
      route idRoute
      compile $ do
        posts <- fmap (take 10) . recentFirstNonDrafts
                   =<< loadAllSnapshots "posts/**" "feed-post-content"
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

indexContext :: PageNumber -> Paginate -> Tags -> Context String
indexContext i pages tags = defaultContext
        <> constField "title" "HOME"
        <> listField "posts" (postContextWithTeaser tags) (takeFromTo start end <$> (recentFirstNonDrafts =<< loadAllSnapshots  "posts/**" "content-for-teaser"))
        <> modificationTimeField "mod" "%Y-%m-%d"
        <> paginateContext pages i
  where
        start = 5 * (i -1)
        end   = 5 * i

feedConfiguration :: FeedConfiguration
feedConfiguration =
  FeedConfiguration
    { feedTitle = "Cascade Of Insights"
    , feedDescription = "Adam Bell's blog"
    , feedAuthorName = "Adam Bell"
    , feedAuthorEmail = "agbell at gmail.com"
    , feedRoot = ""
    }

nonDrafts :: (MonadMetadata m, Functor m) => [Item a] -> m [Item a]
nonDrafts = return. filter f
  where
    f = not . isPrefixOf "posts/drafts/" . show . itemIdentifier

recentFirstNonDrafts :: (MonadMetadata m, Functor m) => [Item a] -> m [Item a]
recentFirstNonDrafts items = do
                       nondrafts <- nonDrafts items
                       recentFirst nondrafts

buildPages :: (MonadMetadata m) => Pattern -> m Paginate
buildPages pattern = buildPaginateWith (return . paginateEvery 5) pattern $ \index ->
   if index == 1
      then fromFilePath "index.html"
      else fromFilePath $ "index/p/" ++ show index ++ ".html"

takeFromTo :: Int -> Int -> [a] -> [a]
takeFromTo start end = drop start . take end
