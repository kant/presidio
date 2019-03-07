import time
import logging

from analyzer.recognizer_registry.recognizers_store_api \
    import RecognizerStoreApi  # noqa: F401

from analyzer.predefined_recognizers import CreditCardRecognizer, \
    SpacyRecognizer, CryptoRecognizer, DomainRecognizer, \
    EmailRecognizer, IbanRecognizer, IpRecognizer, NhsRecognizer, \
    UsBankRecognizer, UsLicenseRecognizer, \
    UsItinRecognizer, UsPassportRecognizer, UsPhoneRecognizer, \
    UsSsnRecognizer


class RecognizerRegistry:
    """
    Detects, registers and holds all recognizers to be used by the analyzer
    """

    def __init__(self, recognizer_store_api=RecognizerStoreApi(),
                 recognizers=[]):
        self.predefined_recognizers = []
        self.recognizers = recognizers
        self.loaded_timestamp = None
        self.loaded_custom_recognizers = []
        self.store_api = recognizer_store_api

        #   TODO: Change the code to dynamic loading -
        # Task #598:  Support loading of the pre-defined recognizers
        # from the given path.
        self.predefined_recognizers.extend([
            CreditCardRecognizer(),
            SpacyRecognizer(),
            CryptoRecognizer(), DomainRecognizer(),
            EmailRecognizer(), IbanRecognizer(),
            IpRecognizer(), NhsRecognizer(),
            UsBankRecognizer(), UsLicenseRecognizer(),
            UsItinRecognizer(), UsPassportRecognizer(),
            UsPhoneRecognizer(), UsSsnRecognizer()])

        self.recognizers.extend(self.predefined_recognizers)

    def get_recognizers(self, entities=None, language=None):
        """
        Returns a list of recognizers, which support the specified name and
        language. if no language and entities are given, all the available
        recognizers will be returned
        :param entities: the requested entities
        :param language: the requested language
        :return: A list of recognizers which support the supplied entities
        and language
        """

        if language is None and entities is None:
            return self.recognizers

        if language is None:
            raise ValueError("No language provided")

        if entities is None:
            raise ValueError("No entities provided")

        to_return = []
        for entity in entities:
            subset = [rec for rec in self.recognizers if
                      entity in rec.supported_entities
                      and language == rec.supported_language]

            if len(subset) == 0:
                logging.warning(
                    "Entity " + entity +
                    " doesn't have the corresponding recognizer in language :"
                    + language)
            else:
                to_return.extend(subset)

        logging.info("Found %d predefined recognizers", len(to_return))
        custom = self.get_custom_recognizers()
        subset_custom = [rec for rec in custom if
                         entity in rec.supported_entities
                         and language == rec.supported_language]
        logging.info("Found %d (total) custom recognizers", len(custom))
        logging.info(
            "Found %d custom recognizers with requested entities and language",
            len(subset_custom))

        if len(subset_custom) > 0:
            to_return.extend(subset_custom)

        logging.info(
            "Returning a total of %d recognizers (predefined + custom)",
            len(to_return))

        if len(to_return) == 0:
            raise ValueError(
                "No matching recognizers were found to serve the request.")

        return to_return

    def get_custom_recognizers(self):
        lst_update = self.store_api.get_latest_timestamp()

        if self.loaded_timestamp is not None:
            logging.info(
                "Analyzer loaded custom recognizers on: %s (%s)",
                time.strftime(
                    '%Y-%m-%d %H:%M:%S',
                    time.localtime(int(self.loaded_timestamp))),
                self.loaded_timestamp)
        else:
            logging.info("Analyzer loaded custom recognizers on: Never")

        # is update time is not set, no custom recognizers in storage, skip
        if lst_update > 0:
            logging.info(
                "Persistent storage was last updated on: %s (%s)",
                time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(lst_update)), lst_update)
            # check if anything updated since last time
            if self.loaded_timestamp is None or \
                    lst_update > self.loaded_timestamp:
                self.loaded_timestamp = int(time.time())

                self.loaded_custom_recognizers = []
                # read all values
                logging.info(
                    "Requesting custom recognizers " +
                    "from persistent storage...")

                raw_recognizers = self.store_api.get_all_recognizers()
                if raw_recognizers is None or len(raw_recognizers) == 0:
                    logging.info(
                        "No custom recognizers found")
                    return []

                for element in raw_recognizers:
                    logging.info("adding: " + element.name)
                    self.loaded_custom_recognizers.append(element)

        return self.loaded_custom_recognizers
