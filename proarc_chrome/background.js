// Patterns til regex: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions
const protekniskRegex = /[A-Z]{3}-[0-9]{2}-[A-Z]-[0-9]{5}/gi;
const fdvRegex = [/SA-[0-9]{6}-[\d]{3}/gi, /KO-[0-9]{6}-[\d]{3}/gi] // finner ikke tegninger uten bladnr
const signalRegex = /S.[0-9]{6}-[\d]{3}/gi; // finner ikke tegninger uten bladnr

function getList (inputStr, searchPattern) {
  return inputStr.match(searchPattern)
}

// This event is fired with the user accepts the input in the omnibox.
chrome.omnibox.onInputEntered.addListener(
    function(text) {
      // Proteknisk arkiv
      results = getList(text, protekniskRegex)
      if (results != null) {
        var protekURL = 'https://proarc.banenor.no/locator.aspx?name=Document.UrlSearch.30&dbrno=12&doc_id=IN(' + encodeURIComponent(results.join(",")) + ')';
        chrome.tabs.create({ url: protekURL });
      }

      // Tegninger med gammelt S-nr, S. blir erstattet med SA-
      var resultArray = [];
      var signalResult = getList(text, signalRegex)
      if (signalResult != null) {
        for (let i=0 ; i < signalResult.length ; i++) {
          signalResult[i] = signalResult[i].replace(/S./gi, "SA-");
        }
        resultArray.push(signalResult.join(","))
      }

      // FDV-arkivet
      var fdvResult;
      for (let i=0 ; i < fdvRegex.length ; i++ ) {
        fdvResult = getList(text, fdvRegex[i]);
        if (fdvResult != null) {
          resultArray.push(fdvResult.join(","));
        }
      }

      if (resultArray.length > 0) {
        let fdvNumbers = resultArray.join(",");
        var fdvURL = 'https://proarc.banenor.no/locator.aspx?name=Document.UrlSearch.30&dbrno=30&doc_id=IN(' + encodeURIComponent(fdvNumbers) + ')';
        chrome.tabs.create({ url: fdvURL });
      }
    }
    )